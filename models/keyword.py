from pydantic import BaseModel, Field
from typing import List

from models.common_options import ToneOption, LengthOption, TargetOption

# keyword 입력 요청 스키마
class KeywordRequest(BaseModel):

    raw_text: str
    tone: ToneOption
    length_option: LengthOption
    target: TargetOption

# 전처리 결과 응답 스키마
class KeywordResponse(BaseModel):
    cleaned_text: str
    keywords: List[str]
    pos_tags: List[str]
    sentence_for_sbert: str

    # 옵션 정보
    tone: ToneOption
    length_option: LengthOption
    target: TargetOption