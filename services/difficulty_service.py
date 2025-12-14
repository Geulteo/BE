import json
from typing import Optional

from openai import OpenAI

from models.difficulty_response import DifficultyDiagnosisResult
from services.difficulty_vector_store import DifficultyVectorStore
from config.settings import get_settings
from core.exceptions import CustomException
from core.error_codes import GlobalErrorCode

from templates.template_hints import TEMPLATE_HINTS

settings = get_settings()

class DifficultyService:
    # 난이도 기준 카드 RAG + GPT를 사용해 난이도를 진단하는 서비스
    def __init__(
        self,
        vector_store: DifficultyVectorStore,
        openai_client: Optional[OpenAI] = None,
    ):
        self.vector_store = vector_store
        self.client = openai_client or OpenAI(api_key=settings.OPENAI_API_KEY)

    @staticmethod
    def _build_query_text(
        sentence_for_sbert: str,
        intent: str,
        target: str,
    ) -> str:
        """template_id를 검색 문장에 굳이 넣지 않아도 됨(카드 검색은 intent 기반)"""
        return (
            f"{target}에게 {intent} 상황에서 작성된 문장의 난이도 기준을 찾습니다. "
            f"문장 의미 요약: {sentence_for_sbert}"
        )

    @staticmethod
    def _build_template_hint_block(template_id: str) -> str:
        """TEMPLATE_HINTS를 프롬프트에 넣기 좋은 문자열로 구성"""
        hint = TEMPLATE_HINTS.get(template_id, {})
        if not hint:
            return ""

        must = hint.get("must_like_advanced", [])
        nice = hint.get("nice_to_have", [])
        extra = hint.get("extra_checklist", [])

        lines = []
        if must:
            lines.append("[템플릿 고급 신호(must_like_advanced)]")
            lines.extend([f"- {m}" for m in must])
        if nice:
            lines.append("\n[추가로 있으면 좋은 요소(nice_to_have)]")
            lines.extend([f"- {n}" for n in nice])
        if extra:
            lines.append("\n[추가 체크리스트(extra_checklist)]")
            lines.extend([f"- {e}" for e in extra])

        return "\n".join(lines).strip()

    def diagnose_difficulty(
        self,
        user_sentence: str,
        sentence_for_sbert: str,
        intent: str,
        template_id: str,
        target: str,
        user_id: Optional[int] = None,  # JWT 기반 사용자를 위한 확장 포인트
    ) -> DifficultyDiagnosisResult:
        """
        난이도 진단 전체 흐름:
        1) RAG로 난이도 기준 카드 검색
        2) 카드 + 사용자 문장을 GPT에 전달
        3) 난이도(level) + 이유(reason) JSON 파싱
        """
        # 1. 난이도 기준 카드 검색 (RAG)
        query_text = self._build_query_text(sentence_for_sbert, intent, template_id)

        hits = self.vector_store.search_cards(
            query_text=query_text,
            intent=intent,
            template_id=None,
            target=target if target else None,
        )

        card_map = {
            point.payload["level"]: point.payload["document"]
            for point in hits.points
        }

        if not card_map:
            raise CustomException(
                GlobalErrorCode.RESOURCE_NOT_FOUND,
                "난이도 기준 카드 검색 결과가 없습니다.",
            )

        template_hint_block = self._build_template_hint_block(template_id)

        # 2. GPT 프롬프트 구성
        prompt = f"""
BEGINNER 기준:
{card_map.get('beginner', '')}

INTERMEDIATE 기준:
{card_map.get('intermediate', '')}

ADVANCED 기준:
{card_map.get('advanced', '')}

{("[템플릿 보정 힌트]\\n" + template_hint_block) if template_hint_block else ""}

[사용자 문장]
{user_sentence}

위 기준을 비교하여 beginner / intermediate / advanced 중 하나를 선택하세요.
그리고 structure / info / tone / fluency 4가지 관점으로 이유를 설명하세요.

반드시 아래 JSON 형식으로만 답변하세요:
{{
  "level": "beginner | intermediate | advanced",
  "reason": {{
      "structure": "...",
      "info": "...",
      "tone": "...",
      "fluency": "..."
  }}
}}
""".strip()

        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "너는 한국어 글쓰기 난이도를 평가하는 조교입니다."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content

        # 3. JSON 파싱 실패 시 공통 에러 코드로 래핑
        try:
            data = json.loads(content)
        except Exception:
            raise CustomException(
                GlobalErrorCode.INTERNAL_SERVER_ERROR,
                "LLM 응답 실패했습니다.",
            )

        return DifficultyDiagnosisResult(**data)
