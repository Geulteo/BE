from pydantic import BaseModel, Field
from typing import Optional, List


class SimilarSentenceRequest(BaseModel):
    text: str = Field(..., description="사용자가 입력한 최종 문장")

    # 추천 정확도를 높이기 위한 선택적 필터
    intent: Optional[str] = Field(None, description="intent 필터 (request/question/...)")
    target: Optional[str] = Field(None, description="target 필터 (professor/friend/...)")
    template_id: Optional[str] = Field(None, description="template_id 필터")