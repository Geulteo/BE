from pydantic import BaseModel, Field
from typing import List

from models.common_options import ToneOption, LengthOption, TargetOption

# 1. 요청 (Request) 모델

# keyword 입력 요청 스키마
class KeywordRequest(BaseModel):

    raw_text: str = Field(..., description="사용자의 키워드 입력 (예: 병원/내일/결석/ 과제 연장)")
    tone: ToneOption = Field("neutral", description="선택된 톤 옵션 (neutral, polite, friendly 중 하나), 기본값 : neutral")
    length_option: LengthOption = Field("normal", description="선택된 길이 옵션 (short, normal, long 중 하나), 기본값 : normal")
    target: TargetOption = Field("professor", description="말하는 대상 (professor, student, friend 중 하나, 기본값 : professor)")

# 2. 응답 (Response) 모델

# 전처리 결과 응답 스키마
class KeywordResponse(BaseModel):
    cleaned_text: str = Field(
        ...,
        description="특수문자 및 다중 공백이 제거된 **정제된 텍스트**"
    )
    keywords: List[str] = Field(
        ...,
        description="형태소 분석을 통해 **추출된 핵심 키워드 리스트**"
    )
    pos_tags: List[str] = Field(
        ...,
        description="추출된 각 키워드에 해당하는 **품사 태그** 리스트"
    )
    sentence_for_sbert: str = Field(
        ...,
        description="SBERT 임베딩을 위해 키워드를 조합하여 생성한 **짧은 문장**"
    )

    # 옵션 정보
    tone: ToneOption = Field(..., description="사용자가 선택한 최종 어조 옵션")
    length_option: LengthOption = Field(..., description="사용자가 선택한 최종 길이 옵션")
    target: TargetOption = Field(..., description="사용자가 선택한 최종 대상 옵션")