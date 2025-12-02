from pydantic import BaseModel, Field
from typing import List, Literal, Optional

from models.common_options import ToneOption, LengthOption, TargetOption

# 1. 요청 (Request) 모델

# keyword 입력 요청 스키마
class KeywordRequest(BaseModel):

    raw_text: str = Field(..., description="사용자의 키워드 입력 (예: 병원/내일/결석/ 과제 연장)")
    tone: ToneOption = Field("neutral", description="선택된 톤 옵션") # 기본값 neutral
    length_option: LengthOption = Field("normal", description="선택된 길이 옵션") # 기본값 normal
    target: TargetOption = Field("professor", description="말하는 대상") # 기본값 professor

# 2. 응답 (Response) 모델

# 전처리 결과 응답 스키마
class keywordResponse(BaseModel):

    cleaned_text: str = Field(..., description="전처리된 텍스트(특수문자/구분자)")
    keywords: List[str] = Field(..., description="추출된 핵심 키워드 리스트")
    pos_tags: List[str] = Field(..., description="키워드 품사 태그")
    sentence_for_sbert: str = Field(..., description="SBERT를 위한 짧은 문장")

    # 옵션 정보
    tone: ToneOption
    length_option: LengthOption
    target: TargetOption