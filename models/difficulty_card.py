from typing import List
from pydantic import BaseModel

from core.level_enums import DifficultyLevel
from core.type_enums import IntentType, TemplateId


class DifficultyCard(BaseModel):
    # 난이도 기준 카드 한 장을 나타내는 모델
    id: str
    intent: IntentType
    template_id: TemplateId
    target: str           # 예: "professor", "friend", "boss"
    level: DifficultyLevel
    title: str
    guide: str
    hint: str             # 사용자에게 보여줄 한 줄 요약
    checklist: List[str]

    def to_prompt_text(self) -> str:
        # 카드를 SBERT·LLM에 넣기 좋은 단일 문자열로 변환
        items = "\n".join(f"- {c}" for c in self.checklist)
        return f"{self.title}\n{self.guide}\n[체크리스트]\n{items}"
