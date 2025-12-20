from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from services.sentence_generator import SentenceGeneratorService
from config.swagger_config import get_current_user
from models.user import User


router = APIRouter(
    prefix="/sentence",
    tags=["sentence"]
)


class SentenceGenerationRequest(BaseModel):
    keywords: List[str] = Field(
        ...,
        description="문장 생성에 사용할 키워드 리스트",
        example=["병원", "내일", "수업"]
    )
    intent: str = Field(
        ...,
        description="문장의 의도",
        example="REQUEST"
    )
    template_id: Optional[str] = Field(
        None,
        description="템플릿 ID",
        example="REQUEST_DEADLINE"
    )
    template_slots: Optional[List[str]] = Field(
        None,
        description="템플릿 구조 요소",
        example=["상황", "이유", "요청", "마무리"]
    )
    tone: Optional[str] = Field(
        "neutral",
        description="문장의 톤 (neutral, polite, business, emotional)",
        example="polite"
    )
    length_option: Optional[str] = Field(
        "normal",
        description="문장 길이 (short, normal, long)",
        example="normal"
    )
    target: Optional[str] = Field(
        "general",
        description="대상",
        example="professor"
    )


class SentenceGenerationResponse(BaseModel):
    generated_sentence: str = Field(
        ...,
        description="생성된 문장",
        example="내일 병원 진료 예약이 있어서 부득이하게 수업에 참석하지 못할 것 같습니다."
    )


class SentenceModificationRequest(BaseModel):
    original_sentence: str = Field(
        ...,
        description="원본 문장",
        example="내일 병원 가야 해서 수업 못 갈 것 같아요."
    )
    modification_type: str = Field(
        ...,
        description="수정 유형 (tone, length, regenerate)",
        example="tone"
    )
    new_value: Optional[str] = Field(
        None,
        description="새로운 값 (tone/length일 때만 필요, regenerate는 불필요)",
        example="business"
    )


class SentenceModificationResponse(BaseModel):
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
    new_value: Optional[str] = Field(
        None,
        description="적용된 새 값",
        example="business"
    )


@router.post(
    "/generate",
    response_model=SentenceGenerationResponse,
    summary="문장 생성",
    description="키워드와 의도, 템플릿 정보를 바탕으로 새로운 문장을 생성합니다."
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
        generated_sentence=generated_sentence
    )


@router.post(
    "/modify",
    response_model=SentenceModificationResponse,
    summary="문장 수정 (톤/길이 변경 또는 재생성)",
    description="기존 문장의 톤이나 길이를 수정하거나, 다른 표현으로 재생성합니다."
)
def modify_sentence(
    request: SentenceModificationRequest,
    current_user: User = Depends(get_current_user)
):
    if request.modification_type not in ["tone", "length", "regenerate"]:
        raise HTTPException(
            status_code=400,
            detail="modification_type은 'tone', 'length', 'regenerate' 중 하나여야 합니다."
        )

    if request.modification_type == "tone":
        valid_tones = ["neutral", "polite", "business", "emotional"]
        if not request.new_value or request.new_value not in valid_tones:
            raise HTTPException(
                status_code=400,
                detail=f"tone은 {', '.join(valid_tones)} 중 하나여야 합니다."
            )

    if request.modification_type == "length":
        valid_lengths = ["short", "normal", "long"]
        if not request.new_value or request.new_value not in valid_lengths:
            raise HTTPException(
                status_code=400,
                detail=f"length는 {', '.join(valid_lengths)} 중 하나여야 합니다."
            )

    service = SentenceGeneratorService()

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
