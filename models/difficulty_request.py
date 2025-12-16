from pydantic import BaseModel
from core.type_enums import IntentType, TemplateId, TargetType


class DifficultyDiagnosisRequest(BaseModel):
    # 난이도 진단 요청 Request
    user_sentence: str
    intent: IntentType
    template_id: TemplateId
    target: TargetType
