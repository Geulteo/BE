"""
훈련 기능
- Mode A: 키워드 기반 작문 연습 (사용자가 직접 작성 → AI 평가)
- Mode B: 톤 변환 연습 (주어진 문장을 특정 톤으로 변환 → AI 평가)
- Session Memory: 이전 시도를 기억하여 점진적 개선 피드백 제공
"""

from openai import OpenAI, OpenAIError
from config.settings import get_settings
from repositories.session_memory import session_memory
from fastapi import HTTPException
import json

settings = get_settings()

# ========== Mode A: 문장 작성 평가 프롬프트 ==========

EVALUATE_WRITING_PROMPT = """
당신은 한국어 글쓰기 교육 전문가입니다.
사용자가 주어진 키워드로 문장을 작성했습니다. 이를 평가하고 피드백을 제공하세요.

[주어진 키워드]
{keywords}

[의도(Intent)]
{intent}
- request: 요청, question: 질문, notice: 공지, apology: 사과, complaint: 불만/신고

[템플릿]
{template_id}
- request_deadline: 마감 연장 요청
- request_absence: 결석 양해 요청
- request_help: 도움 요청
- request_info: 자료 요청

[말하는 대상]
{target}
- professor: 교수님
- senior_junior: 선/후배
- friend: 친구
- boss: 직장 상사

[사용자가 작성한 문장]
{user_sentence}

{history_text}

[평가 기준]
1. 정중함(politeness): 대상에 맞는 어투와 존댓말 사용 정도 (0~100점)
2. 명확성(clarity): 의도와 상황이 명확하게 전달되는지 (0~100점)
3. 이해도(understanding): 상대방이 쉽게 이해할 수 있는 문장인지 (0~100점)

[피드백 항목]
- structure: 문장 구조 평가 (상황-이유-요청-마무리 흐름이 있는지)
- tone: 톤의 적절성 (대상에 맞는 존댓말과 표현 사용 여부)
- missing_info: 빠진 정보나 추가하면 좋을 내용

[이전 시도 대비 개선점]
이전 시도가 있다면, 어떤 부분이 좋아졌는지/아직 부족한지 구체적으로 설명하세요.
이전 시도가 없다면 빈 문자열("")로 남겨두세요.

[AI 제안 문장]
더 나은 버전의 문장을 제시하세요. 사용자 문장의 의미를 유지하되, 평가 기준에 따라 개선된 버전을 작성하세요.

다음 JSON 형식으로만 답하세요:
{{
  "scores": {{
    "politeness": 0~100,
    "clarity": 0~100,
    "understanding": 0~100
  }},
  "feedback": {{
    "structure": "문장 구조에 대한 평가 (1~2문장)",
    "tone": "톤의 적절성에 대한 평가 (1~2문장)",
    "missing_info": "빠진 정보나 추가하면 좋을 내용 (1~2문장)"
  }},
  "ai_suggestion": "개선된 문장 전체",
  "improvement_from_previous": "이전 시도 대비 개선점 (있으면 작성, 없으면 빈 문자열)"
}}
"""


# ========== Mode B: 톤 변환 평가 프롬프트 ==========

EVALUATE_TONE_CONVERSION_PROMPT = """
당신은 한국어 문체 교육 전문가입니다.
사용자가 주어진 문장을 특정 톤으로 변환하는 연습을 하고 있습니다.

[원본 문장]
{original_sentence}

[목표 톤]
{target_tone}
- neutral: 중립적, 객관적
- polite: 정중하고 공손함
- business: 비즈니스, 공식적
- emotional: 따뜻하고 감성적

[말하는 대상]
{target}
- professor: 교수님
- senior_junior: 선/후배
- friend: 친구
- boss: 직장 상사

[사용자가 수정한 문장]
{user_modified_sentence}

{history_text}

[평가 항목]
1. 목표 톤에 맞게 수정했는지
2. 대상에 맞는 어투인지
3. 원본 의미를 유지했는지
4. 더 개선할 점이 있는지

[피드백 작성]
- 사용자가 잘한 점과 부족한 점을 구체적으로 설명하세요.
- 이전 시도가 있다면, 어떤 부분이 개선되었는지 언급하세요.

[개선 제안]
- 더 나아질 수 있는 구체적인 방법을 1~3개 제시하세요.

[예시 문장]
- 사용자 문장을 바탕으로 목표 톤에 더 적합한 예시 문장을 제시하세요.

다음 JSON 형식으로만 답하세요:
{{
  "is_appropriate": true 또는 false (목표 톤에 적합한지),
  "feedback": "전체 피드백 (3~5문장)",
  "suggestions": ["개선 제안 1", "개선 제안 2", "개선 제안 3"],
  "example_sentence": "개선된 예시 문장",
  "improvement_from_previous": "이전 시도 대비 개선점 (있으면 작성, 없으면 빈 문자열)"
}}
"""


class TrainingService:

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def evaluate_user_sentence(
        self,
        session_id: str,
        user_sentence: str,
        keywords: list[str],
        intent: str,
        template_id: str,
        target: str
    ) -> dict:
        try:
            # 1. 이전 시도 히스토리 가져오기
            history = session_memory.get_history(session_id, last_n=3)

            # 2. 히스토리를 프롬프트에 포함
            history_text = self._format_history(history)

            # 3. 평가 프롬프트 구성
            prompt = EVALUATE_WRITING_PROMPT.format(
                keywords=", ".join(keywords),
                intent=intent,
                template_id=template_id,
                target=target,
                user_sentence=user_sentence,
                history_text=history_text
            )

            # 4. GPT API 호출
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 한국어 글쓰기 평가 전문가입니다."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,  # 평가는 일관성이 중요하므로 낮은 temperature
                max_tokens=800,
                response_format={"type": "json_object"}
            )

            # 5. JSON 파싱
            result = json.loads(response.choices[0].message.content)

            # 6. 세션 메모리에 저장
            turn_number = len(history) + 1
            session_memory.add_turn(session_id, {
                "turn": turn_number,
                "user_sentence": user_sentence,
                "ai_feedback": result["feedback"],
                "ai_suggestion": result["ai_suggestion"],
                "scores": result["scores"]
            })

            return result

        except OpenAIError as e:
            print(f"OpenAI API Error in evaluate_user_sentence: {e}")
            raise HTTPException(
                status_code=503,
                detail="AI 평가 서비스 일시적 오류입니다. 잠시 후 다시 시도해주세요."
            )
        except json.JSONDecodeError as e:
            print(f"JSON parsing error in evaluate_user_sentence: {e}")
            raise HTTPException(
                status_code=500,
                detail="AI 응답 파싱 중 오류가 발생했습니다."
            )
        except Exception as e:
            print(f"Unexpected error in evaluate_user_sentence: {e}")
            raise HTTPException(
                status_code=500,
                detail="문장 평가 중 오류가 발생했습니다."
            )

    def evaluate_tone_conversion(
        self,
        session_id: str,
        original_sentence: str,
        user_modified_sentence: str,
        target_tone: str,
        target: str
    ) -> dict:

        try:
            # 이전 시도 히스토리 가져오기
            history = session_memory.get_history(session_id, last_n=2)

            # 히스토리를 프롬프트에 포함
            history_text = self._format_history(history)

            # 평가 프롬프트 구성
            prompt = EVALUATE_TONE_CONVERSION_PROMPT.format(
                original_sentence=original_sentence,
                target_tone=target_tone,
                target=target,
                user_modified_sentence=user_modified_sentence,
                history_text=history_text
            )

            # GPT API 호출
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 문체 변환 평가 전문가입니다."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=600,
                response_format={"type": "json_object"}
            )

            # JSON 
            result = json.loads(response.choices[0].message.content)

            # 세션 메모리에 저장
            turn_number = len(history) + 1
            session_memory.add_turn(session_id, {
                "turn": turn_number,
                "user_sentence": user_modified_sentence,
                "ai_feedback": result["feedback"],
                "ai_suggestion": result.get("example_sentence", ""),
                "is_appropriate": result["is_appropriate"]
            })

            return result

        except OpenAIError as e:
            print(f"OpenAI API Error in evaluate_tone_conversion: {e}")
            raise HTTPException(
                status_code=503,
                detail="AI 평가 서비스 일시적 오류입니다. 잠시 후 다시 시도해주세요."
            )
        except json.JSONDecodeError as e:
            print(f"JSON parsing error in evaluate_tone_conversion: {e}")
            raise HTTPException(
                status_code=500,
                detail="AI 응답 파싱 중 오류가 발생했습니다."
            )
        except Exception as e:
            print(f"Unexpected error in evaluate_tone_conversion: {e}")
            raise HTTPException(
                status_code=500,
                detail="톤 변환 평가 중 오류가 발생했습니다."
            )

    def _format_history(self, history: list) -> str:
        if not history:
            return "[이전 시도 없음]"

        formatted = "[이전 시도 히스토리]\n"
        for h in history:
            formatted += f"{h['turn']}번 시도: {h['user_sentence']}\n"

            # ai_feedback이 dict인 경우와 str인 경우 모두 처리
            if isinstance(h.get('ai_feedback'), dict):
                feedback_summary = " / ".join([
                    f"{key}: {value}"
                    for key, value in h['ai_feedback'].items()
                ])
            else:
                feedback_summary = str(h.get('ai_feedback', ''))

            formatted += f"  → AI 피드백: {feedback_summary}\n\n"

        return formatted
