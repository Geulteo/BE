from pydantic import BaseModel, Field
from typing import Optional, List

class SimilarSentenceRequest(BaseModel):
    text: str

    # 추천 정확도를 높이기 위한 선택적 필터
    intent: Optional[str]
    target: Optional[str]
    template_id: Optional[str]