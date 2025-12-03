from pydantic import BaseModel
from core.type_enums import IntentType, TemplateId


class DifficultyDiagnosisRequest(BaseModel):\
    # 난이도 진단 요청 Request
    user_sentence: str # 사용자가 실제로 쓴 문장
    intent: IntentType
    template_id: TemplateId
    target: str  # 예: "professor", "friend", "boss"
