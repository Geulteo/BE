from openai import OpenAI, OpenAIError
from config.settings import get_settings
from fastapi import HTTPException
import json

settings = get_settings()

# 문장 생성 프롬프트 템플릿
SENTENCE_GENERATION_PROMPT = """
당신은 한국어 글쓰기 도우미입니다.
사용자가 전달한 상황 정보, 키워드, 톤, 말하는 대상(Target)을 바탕으로
가장 자연스럽고 매끄러운 문장을 생성하는 역할을 합니다.

아래 정보를 기반으로 문장을 작성하세요.

[의도(Intent)]
{intent_label}
예: 요청(Request), 질문(Question), 공지(Notice), 사과(Apology), 불만/신고(Complaint)

[세부 템플릿 유형(Template)]
{template_name}
예: request_deadline(마감 연장 요청), request_absence(결석 양해 요청) 등

[문장 구성 흐름(Template Slots)]
{slot_list}
- 위 구성 흐름(슬롯)을 반드시 순서대로 따르세요.
- 각 슬롯은 한 문장 또는 자연스러운 짧은 구로 표현하세요.

[사용자 키워드]
{keywords}
위 키워드들은 문장 안에 반드시 자연스럽게 포함되어야 합니다.

[톤(Tone)]
{tone}
예: neutral, polite, business, emotional

[말하는 대상(Target)]
{target}
예: 교수님, 선/후배, 친구, 직장 상사
- 대상에 맞게 존댓말/반말, 말투의 공손함 수준, 표현 방식 등을 조정하세요.

[길이 옵션(Length)]
{length_option}
예: short(짧게), normal(보통), long(자세하게)
- 선택된 옵션에 따라 문장 길이를 조절하세요:
  - short: 1~2문장
  - normal: 2~4문장
  - long: 4~6문장

[작성 규칙]
1. 템플릿 흐름(slot_list)에 따라 논리적으로 연결되게 작성할 것.
2. 사용자 키워드의 의미를 훼손하지 말고 자연스럽게 재구성할 것.
3. 말하는 대상(target)에 어울리는 어투와 예절 수준을 정확히 반영할 것.
4. 전체 문장은 length 옵션에 맞춰 적절한 분량으로 조절할 것.
5. 한국어 문맥과 자연스러운 흐름을 유지할 것.
6. tone에 따라 문장 스타일(정중함/감성/비즈니스)을 확실히 지킬 것.

이제 위 정보를 모두 반영하여 자연스러운 문장을 생성하세요.
생성된 문장만 출력하고 다른 설명은 하지 마세요.
"""


# 톤 수정 프롬프트 템플릿
TONE_MODIFICATION_PROMPT = """
아래 문장의 톤을 '{new_tone}'로 수정해주세요.

[원본 문장]
{original_sentence}

[요청사항]
- 내용과 의미는 그대로 유지
- 톤만 '{new_tone}' 스타일로 변경
- 톤 종류:
  - neutral: 중립적, 객관적
  - polite: 정중하고 공손함
  - business: 비즈니스, 공식적
  - emotional: 따뜻하고 감성적

수정된 문장만 출력하고 다른 설명은 하지 마세요.
"""


# 길이 수정 프롬프트 템플릿
LENGTH_MODIFICATION_PROMPT = """
아래 문장의 길이를 '{new_length}'로 수정해주세요.

[원본 문장]
{original_sentence}

[요청사항]
- 핵심 의미는 그대로 유지
- 길이만 '{new_length}' 스타일로 변경
- 길이 옵션:
  - short: 1~2문장으로 간결하게
  - normal: 2~4문장으로 적당히
  - long: 4~6문장으로 자세하게

수정된 문장만 출력하고 다른 설명은 하지 마세요.
"""


class SentenceGeneratorService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL 

    def generate_sentence(
        self,
        keywords: list[str],
        intent: str,
        template_id: str,
        template_slots: list[str],
        tone: str,
        length_option: str,
        target: str
    ) -> str:
        try:
            # Prompt 채우기
            prompt = SENTENCE_GENERATION_PROMPT.format(
                intent_label=intent,
                template_name=template_id,
                slot_list=" → ".join(template_slots),
                keywords=", ".join(keywords),
                tone=tone,
                length_option=length_option,
                target=target
            )

            # GPT API 호출
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 한국어 글쓰기 전문가입니다."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )

            generated_sentence = response.choices[0].message.content.strip()
            return generated_sentence

        except OpenAIError as e:
            # OpenAI API 에러 처리
            print(f"OpenAI API Error in generate_sentence: {e}")
            raise HTTPException(
                status_code=503,
                detail="AI 서비스 일시적 오류입니다. 잠시 후 다시 시도해주세요."
            )
        except Exception as e:
            # 기타 예외 처리
            print(f"Unexpected error in generate_sentence: {e}")
            raise HTTPException(
                status_code=500,
                detail="문장 생성 중 오류가 발생했습니다."
            )

    def modify_sentence(
        self,
        original_sentence: str,
        modification_type: str,  
        new_value: str  
    ) -> str:
        try:
            # 수정 타입에 따라 프롬프트 선택
            if modification_type == "tone":
                prompt = TONE_MODIFICATION_PROMPT.format(
                    original_sentence=original_sentence,
                    new_tone=new_value
                )
            elif modification_type == "length":
                prompt = LENGTH_MODIFICATION_PROMPT.format(
                    original_sentence=original_sentence,
                    new_length=new_value
                )
            else:
                raise ValueError(f"Invalid modification_type: {modification_type}")

            # GPT API 호출
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 한국어 문장 수정 전문가입니다."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )

            modified_sentence = response.choices[0].message.content.strip()
            return modified_sentence

        except OpenAIError as e:
            # OpenAI API 에러 처리
            print(f"OpenAI API Error in modify_sentence: {e}")
            raise HTTPException(
                status_code=503,
                detail="AI 서비스 일시적 오류입니다. 잠시 후 다시 시도해주세요."
            )
        except ValueError as e:
            print(f"Invalid parameter in modify_sentence: {e}")
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            # 기타 예외 처리
            print(f"Unexpected error in modify_sentence: {e}")
            raise HTTPException(
                status_code=500,
                detail="문장 수정 중 오류가 발생했습니다."
            )

    def regenerate_sentence(
        self,
        keywords: list[str],
        intent: str,
        template_id: str,
        template_slots: list[str],
        tone: str,
        length_option: str,
        target: str
    ) -> str:
        try:
            prompt = SENTENCE_GENERATION_PROMPT.format(
                intent_label=intent,
                template_name=template_id,
                slot_list=" → ".join(template_slots),
                keywords=", ".join(keywords),
                tone=tone,
                length_option=length_option,
                target=target
            )

            # temperature를 높여서 더 다양한 결과 생성
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 한국어 글쓰기 전문가입니다. 창의적이고 다양한 표현을 사용하세요."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.9,  # 더 높은 창의성
                max_tokens=500
            )

            regenerated_sentence = response.choices[0].message.content.strip()
            return regenerated_sentence

        except OpenAIError as e:
            print(f"OpenAI API Error in regenerate_sentence: {e}")
            raise HTTPException(
                status_code=503,
                detail="AI 서비스 일시적 오류입니다. 잠시 후 다시 시도해주세요."
            )
        except Exception as e:
            print(f"Unexpected error in regenerate_sentence: {e}")
            raise HTTPException(
                status_code=500,
                detail="문장 재생성 중 오류가 발생했습니다."
            )
