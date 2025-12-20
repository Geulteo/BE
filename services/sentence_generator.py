from openai import OpenAI, OpenAIError
from config.settings import get_settings
from fastapi import HTTPException

settings = get_settings()

ENHANCED_SYSTEM_PROMPT = """
당신은 한국어 글쓰기 전문 AI 어시스턴트입니다.

## 역할 및 전문성
- 한국어 문법, 어휘, 문체에 대한 전문적 지식 보유
- 상황별(학업, 비즈니스, 일상) 적절한 표현 추천 능력
- 대상(교수님, 상사, 친구 등)에 따른 존대법 및 어투 조절 능력
- 사용자의 의도를 파악하여 맥락에 맞는 자연스러운 문장 생성

## 행동 원칙
1. 의도 파악: 사용자가 전달하고자 하는 핵심 메시지를 정확히 이해합니다.
2. 맥락 고려: 대화 상대, 상황, 목적을 종합적으로 고려합니다.
3. 톤앤매너 준수: 요청된 톤(정중함, 비즈니스, 감성적 등)을 정확히 반영합니다.
4. 문화적 적절성: 한국 문화와 사회적 맥락에 맞는 표현을 사용합니다.
5. 명확성과 간결성: 불필요한 수식어를 피하고 핵심을 전달합니다.

## 품질 기준
- 문법적으로 정확한 문장
- 자연스럽고 어색하지 않은 흐름
- 요청된 길이와 형식 준수
- 키워드의 의미를 훼손하지 않는 자연스러운 통합
"""

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

REGENERATE_PROMPT = """
아래 문장을 같은 의미와 톤을 유지하면서 다른 표현으로 다시 작성해주세요.

[원본 문장]
{original_sentence}

[요청사항]
- 핵심 의미와 의도는 그대로 유지
- 다른 어휘와 표현 방식 사용
- 문장 구조를 창의적으로 변경
- 자연스럽고 매끄러운 한국어 유지

새로 작성된 문장만 출력하고 다른 설명은 하지 마세요.
"""

SENTENCE_GENERATION_PROMPT = """
다음 정보를 바탕으로 자연스러운 한국어 문장을 생성해주세요.

[키워드]
{keywords}

[의도 (Intent)]
{intent}

[템플릿 구조]
템플릿 ID: {template_id}
구조 요소: {template_slots}

[스타일 요구사항]
- 톤: {tone}
- 길이: {length_option}
- 대상: {target}

[생성 지침]
1. 제공된 키워드를 자연스럽게 포함시키세요
2. 의도(Intent)에 맞는 문장 구조를 사용하세요
3. 템플릿 구조를 참고하여 논리적 흐름을 구성하세요
4. 요청된 톤과 길이에 맞게 작성하세요
5. 대상에 맞는 존대법과 어투를 사용하세요
6. 문법적으로 정확하고 자연스러운 한국어를 사용하세요

생성된 문장만 출력하고 다른 설명은 하지 마세요.
"""


class SentenceGeneratorService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def generate_sentence(
        self,
        keywords: list,
        intent: str,
        template_id: str = None,
        template_slots: list = None,
        tone: str = "neutral",
        length_option: str = "normal",
        target: str = "general"
    ) -> str:
        """
        키워드와 의도, 템플릿 정보를 바탕으로 새로운 문장을 생성합니다.

        Args:
            keywords: 문장에 포함할 키워드 리스트
            intent: 문장의 의도 (예: REQUEST, INFORM, APOLOGY 등)
            template_id: 템플릿 ID (선택사항)
            template_slots: 템플릿 구조 요소 (선택사항)
            tone: 문장의 톤 (neutral, polite, business, emotional)
            length_option: 문장 길이 (short, normal, long)
            target: 대상 (general, professor, boss, friend 등)

        Returns:
            생성된 문장 (str)
        """
        try:
            # 키워드를 문자열로 변환
            keywords_str = ", ".join(keywords) if isinstance(keywords, list) else str(keywords)

            # 템플릿 슬롯을 문자열로 변환
            template_slots_str = ", ".join(template_slots) if template_slots else "없음"

            # 프롬프트 생성
            prompt = SENTENCE_GENERATION_PROMPT.format(
                keywords=keywords_str,
                intent=intent or "일반",
                template_id=template_id or "없음",
                template_slots=template_slots_str,
                tone=tone or "neutral",
                length_option=length_option or "normal",
                target=target or "general"
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": ENHANCED_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )

            generated_sentence = response.choices[0].message.content.strip()

            if not generated_sentence:
                raise ValueError("Generated sentence is empty")

            return generated_sentence

        except OpenAIError as e:
            print(f"OpenAI API Error in generate_sentence: {e}")
            raise HTTPException(
                status_code=503,
                detail="AI 서비스 일시적 오류입니다. 잠시 후 다시 시도해주세요."
            )
        except Exception as e:
            print(f"Unexpected error in generate_sentence: {e}")
            raise HTTPException(
                status_code=500,
                detail="문장 생성 중 오류가 발생했습니다."
            )

    def modify_sentence(
        self,
        original_sentence: str,
        modification_type: str,
        new_value: str = None
    ) -> str:
        try:
            if modification_type == "tone":
                prompt = TONE_MODIFICATION_PROMPT.format(
                    original_sentence=original_sentence,
                    new_tone=new_value
                )
                temperature = 0.7
            elif modification_type == "length":
                prompt = LENGTH_MODIFICATION_PROMPT.format(
                    original_sentence=original_sentence,
                    new_length=new_value
                )
                temperature = 0.7
            elif modification_type == "regenerate":
                prompt = REGENERATE_PROMPT.format(
                    original_sentence=original_sentence
                )
                temperature = 0.9
            else:
                raise ValueError(f"Invalid modification_type: {modification_type}")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": ENHANCED_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()

        except OpenAIError as e:
            print(f"OpenAI API Error in modify_sentence: {e}")
            raise HTTPException(
                status_code=503,
                detail="AI 서비스 일시적 오류입니다. 잠시 후 다시 시도해주세요."
            )
        except ValueError as e:
            print(f"Invalid parameter in modify_sentence: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            print(f"Unexpected error in modify_sentence: {e}")
            raise HTTPException(
                status_code=500,
                detail="문장 수정 중 오류가 발생했습니다."
            )
