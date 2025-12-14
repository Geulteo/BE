from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List
from services.sentence_generator import SentenceGeneratorService
from config.swagger_config import get_current_user
from models.user import User


router = APIRouter(
    prefix="/sentence",
    tags=["sentence"]
)

class SentenceGenerationRequest(BaseModel):
    """문장 생성 요청 모델"""
    keywords: List[str] = Field(
        ...,
        description="사용자 키워드 리스트",
        example=["병원", "내일", "결석", "과제", "연장"]
    )
    intent: str = Field(
        ...,
        description="Intent 유형 (request, question, notice, apology, complaint)",
        example="request"
    )
    template_id: str = Field(
        ...,
        description="템플릿 ID (request_deadline, request_absence, etc.)",
        example="request_deadline"
    )
    template_slots: List[str] = Field(
        ...,
        description="템플릿 구성 흐름",
        example=["상황", "이유", "요청", "마무리"]
    )
    tone: str = Field(
        ...,
        description="톤 (neutral, polite, business, emotional)",
        example="polite"
    )
    length_option: str = Field(
        ...,
        description="길이 옵션 (short, normal, long)",
        example="normal"
    )
    target: str = Field(
        ...,
        description="말하는 대상 (professor, senior_junior, friend, boss)",
        example="professor"
    )


class SentenceGenerationResponse(BaseModel):
    """문장 생성 응답 모델"""
    generated_sentence: str = Field(
        ...,
        description="생성된 문장",
        example="교수님, 안녕하세요. 내일 병원 예약이 있어 부득이하게 수업에 결석하게 될 것 같습니다. 이에 따라 과제 제출 기한을 조금 연장해주실 수 있을까요? 양해 부탁드립니다."
    )
    tone_used: str = Field(
        ...,
        description="사용된 톤",
        example="polite"
    )
    length_used: str = Field(
        ...,
        description="사용된 길이 옵션",
        example="normal"
    )
    target_used: str = Field(
        ...,
        description="대상",
        example="professor"
    )


class SentenceModificationRequest(BaseModel):
    """문장 수정 요청 모델"""
    original_sentence: str = Field(
        ...,
        description="원본 문장",
        example="내일 병원 가야 해서 수업 못 갈 것 같아요."
    )
    modification_type: str = Field(
        ...,
        description="수정 유형 (tone 또는 length)",
        example="tone"
    )
    new_value: str = Field(
        ...,
        description="새로운 값 (tone: neutral/polite/business/emotional, length: short/normal/long)",
        example="business"
    )


class SentenceModificationResponse(BaseModel):
    """문장 수정 응답 모델"""
    modified_sentence: str = Field(
        ...,
        description="수정된 문장",
        example="내일 부득이한 사정으로 수업에 참석하지 못할 것 같습니다."
    )
    modification_type: str = Field(
        ...,
        description="수정 유형",
        example="tone"
    )
    new_value: str = Field(
        ...,
        description="적용된 새 값",
        example="business"
    )

@router.post(
    "/generate",
    response_model=SentenceGenerationResponse,
    summary="키워드 기반 문장 생성",
    description="""
    사용자가 입력한 키워드를 기반으로 자연스러운 문장을 생성합니다.

    GPT-4o-mini를 사용하여 Intent, Template, Tone, Length, Target을 고려한 문장을 생성합니다.
    """
)
def generate_sentence(
    request: SentenceGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    service = SentenceGeneratorService()

    generated_sentence = service.generate_sentence(
        keywords=request.keywords,
        intent=request.intent,
        template_id=request.template_id,
        template_slots=request.template_slots,
        tone=request.tone,
        length_option=request.length_option,
        target=request.target
    )

    return SentenceGenerationResponse(
        generated_sentence=generated_sentence,
        tone_used=request.tone,
        length_used=request.length_option,
        target_used=request.target
    )


@router.post(
    "/modify",
    response_model=SentenceModificationResponse,
    summary="문장 수정 (톤/길이 변경)",
    description="""
    기존 문장의 톤이나 길이를 수정합니다.

    - **톤 변경**: neutral, polite, business, emotional 중 선택
    - **길이 변경**: short, normal, long 중 선택
    """
)
def modify_sentence(
    request: SentenceModificationRequest,
    current_user: User = Depends(get_current_user)
):
    # 입력 검증
    if request.modification_type not in ["tone", "length"]:
        raise HTTPException(
            status_code=400,
            detail="modification_type은 'tone' 또는 'length'여야 합니다."
        )

    if request.modification_type == "tone":
        valid_tones = ["neutral", "polite", "business", "emotional"]
        if request.new_value not in valid_tones:
            raise HTTPException(
                status_code=400,
                detail=f"tone은 {', '.join(valid_tones)} 중 하나여야 합니다."
            )

    if request.modification_type == "length":
        valid_lengths = ["short", "normal", "long"]
        if request.new_value not in valid_lengths:
            raise HTTPException(
                status_code=400,
                detail=f"length는 {', '.join(valid_lengths)} 중 하나여야 합니다."
            )

    service = SentenceGeneratorService()

    # 문장 수정
    modified_sentence = service.modify_sentence(
        original_sentence=request.original_sentence,
        modification_type=request.modification_type,
        new_value=request.new_value
    )

    return SentenceModificationResponse(
        modified_sentence=modified_sentence,
        modification_type=request.modification_type,
        new_value=request.new_value
    )


@router.post(
    "/regenerate",
    response_model=SentenceGenerationResponse,
    summary="문장 재생성",
    description="""
    동일한 조건으로 문장을 다시 생성합니다.

    사용자가 생성된 문장이 마음에 들지 않을 때 사용합니다.
    기존 generate와 동일하지만 temperature를 높여 더 다양한 표현을 생성합니다.
    """
)
def regenerate_sentence(
    request: SentenceGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    service = SentenceGeneratorService()

    # 문장 재생성
    regenerated_sentence = service.regenerate_sentence(
        keywords=request.keywords,
        intent=request.intent,
        template_id=request.template_id,
        template_slots=request.template_slots,
        tone=request.tone,
        length_option=request.length_option,
        target=request.target
    )

    return SentenceGenerationResponse(
        generated_sentence=regenerated_sentence,
        tone_used=request.tone,
        length_used=request.length_option,
        target_used=request.target
    )
