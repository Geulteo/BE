from pydantic import BaseModel, Field
from typing import Optional, List

class SimilarSentenceItem(BaseModel):
    text: str = Field(..., description="과거에 작성했던 문장")
    score: float = Field(..., description="유사도 점수 (cosine similarity)")

    created_at: Optional[str] = Field(None, description="작성 시각")

    # 메타 정보 (표시 or 내부 분석용)
    intent: Optional[str] = None
    target: Optional[str] = None
    template_id: Optional[str] = None

class SimilarSentenceResponse(BaseModel):
    recommendations: List[SimilarSentenceItem]
