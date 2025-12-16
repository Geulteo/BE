from pydantic import BaseModel, Field
from typing import Optional, List

class SimilarSentenceItem(BaseModel):
    text: str
    score: float

    created_at: Optional[str]

    # 메타 정보 (표시 or 내부 분석용)
    intent: Optional[str] = None
    target: Optional[str] = None
    template_id: Optional[str] = None

class SimilarSentenceResponse(BaseModel):
    recommendations: List[SimilarSentenceItem]
