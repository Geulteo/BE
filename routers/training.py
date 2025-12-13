"""
훈련 API 라우터

사용자의 문장 작성 연습을 평가하고 피드백을 제공하는 API 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from services.training_service import TrainingService
from config.swagger_config import get_current_user
from models.user import User
import uuid


router = APIRouter(
    prefix="/training",
    tags=["training"]
)

class WritePracticeRequest(BaseModel):
    session_id: Optional[str] = Field(
        None,
        description="세션 ID (없으면 자동 생성)"
    )
    keywords: List[str] = Field(
        ...,
        description="주어진 키워드",
        example=["병원", "내일", "결석", "과제", "연장"]
    )
    user_sentence: str = Field(
        ...,
        description="사용자가 작성한 문장",
        example="내일 병원 가야 해서 수업 못 갈 것 같은데 과제도 좀 봐주세요"
    )
    intent: str = Field(
        ...,
        description="의도 (request, question, notice, apology, complaint)",
        example="request"
    )
    template_id: str = Field(
        ...,
        description="템플릿 ID (request_deadline, request_absence, etc.)",
        example="request_deadline"
    )
    target: str = Field(
        ...,
        description="대상 (professor, senior_junior, friend, boss)",
        example="professor"
    )


class WritePracticeResponse(BaseModel):
    session_id: str = Field(
        ...,
        description="세션 ID (다음 시도에서 재사용)"
    )
    scores: Dict[str, int] = Field(
        ...,
        description="평가 점수 (politeness, clarity, understanding)",
        example={"politeness": 60, "clarity": 80, "understanding": 75}
    )
    feedback: Dict[str, str] = Field(
        ...,
        description="피드백 (structure, tone, missing_info)",
        example={
            "structure": "상황-이유-요청 흐름은 있지만, 마무리 인사가 부족합니다.",
            "tone": "교수님께 드리는 글치고는 다소 캐주얼한 표현이 있습니다.",
            "missing_info": "구체적인 날짜와 과목명을 추가하면 좋습니다."
        }
    )
    ai_suggestion: str = Field(
        ...,
        description="AI가 제안하는 개선된 문장",
        example="교수님, 안녕하세요. 내일 병원 예약이 있어 부득이하게 수업에 결석하게 될 것 같습니다. 이에 따라 과제 제출 기한을 조금 연장해주실 수 있을까요? 양해 부탁드립니다."
    )
    improvement_from_previous: str = Field(
        "",
        description="이전 시도 대비 개선점 (이전 시도가 없으면 빈 문자열)",
        example="이전 시도보다 이유가 명확해졌습니다."
    )


# ----- Mode B: 톤 변환 평가 -----

class ToneConversionRequest(BaseModel):
    session_id: Optional[str] = Field(
        None,
        description="세션 ID (없으면 자동 생성)"
    )
    original_sentence: str = Field(
        ...,
        description="원본 문장",
        example="내일 수업 못 갈 것 같습니다."
    )
    user_modified_sentence: str = Field(
        ...,
        description="사용자가 수정한 문장",
        example="교수님, 내일 부득이한 사정으로 수업에 참석하지 못할 것 같습니다."
    )
    target_tone: str = Field(
        ...,
        description="목표 톤 (neutral, polite, business, emotional)",
        example="business"
    )
    target: str = Field(
        ...,
        description="대상 (professor, senior_junior, friend, boss)",
        example="professor"
    )


class ToneConversionResponse(BaseModel):
    session_id: str = Field(
        ...,
        description="세션 ID"
    )
    is_appropriate: bool = Field(
        ...,
        description="목표 톤에 적합한지 여부",
        example=True
    )
    feedback: str = Field(
        ...,
        description="전체 피드백",
        example="비즈니스 톤으로 잘 수정하셨습니다. '부득이한 사정'이라는 표현이 적절합니다."
    )
    suggestions: List[str] = Field(
        ...,
        description="개선 제안 리스트",
        example=[
            "마무리 인사를 추가하면 더욱 완성도가 높아집니다.",
            "예: '양해 부탁드립니다.' 또는 '감사합니다.'"
        ]
    )
    example_sentence: str = Field(
        ...,
        description="AI가 제안하는 예시 문장",
        example="교수님, 내일 부득이한 사정으로 수업에 참석하지 못할 것 같습니다. 양해 부탁드립니다."
    )
    improvement_from_previous: str = Field(
        "",
        description="이전 시도 대비 개선점",
        example="이전보다 존댓말 사용이 더 자연스러워졌습니다."
    )

@router.post(
    "/practice/write",
    response_model=WritePracticeResponse,
    summary="문장 작성 연습 평가 (Mode A)",
    description="""
    사용자가 키워드를 바탕으로 직접 작성한 문장을 평가합니다.

    - 정중함, 명확성, 이해도 점수 제공
    - 구조, 톤, 빠진 정보에 대한 피드백
    - AI가 제안하는 개선된 문장
    - 세션 내 이전 시도 대비 개선점 (Session Memory 활용)
    """
)
def practice_writing(
    request: WritePracticeRequest,
    current_user: User = Depends(get_current_user)
):
    # 세션 ID 생성 또는 재사용
    session_id = request.session_id or str(uuid.uuid4())

    # Service 인스턴스 생성
    service = TrainingService()

    # 문장 평가
    result = service.evaluate_user_sentence(
        session_id=session_id,
        user_sentence=request.user_sentence,
        keywords=request.keywords,
        intent=request.intent,
        template_id=request.template_id,
        target=request.target
    )

    return WritePracticeResponse(
        session_id=session_id,
        scores=result["scores"],
        feedback=result["feedback"],
        ai_suggestion=result["ai_suggestion"],
        improvement_from_previous=result.get("improvement_from_previous", "")
    )


@router.post(
    "/practice/tone",
    response_model=ToneConversionResponse,
    summary="톤 변환 연습 평가 (Mode B)",
    description="""
    사용자가 주어진 문장을 특정 톤으로 변환한 결과를 평가합니다.

    - 목표 톤에 적합한지 여부
    - 구체적인 피드백
    - 개선 제안 리스트
    - AI가 제안하는 예시 문장
    - 세션 내 이전 시도 대비 개선점
    """
)
def practice_tone_conversion(
    request: ToneConversionRequest,
    current_user: User = Depends(get_current_user)
):
    # 입력 검증
    valid_tones = ["neutral", "polite", "business", "emotional"]
    if request.target_tone not in valid_tones:
        raise HTTPException(
            status_code=400,
            detail=f"target_tone은 {', '.join(valid_tones)} 중 하나여야 합니다."
        )

    valid_targets = ["professor", "senior_junior", "friend", "boss"]
    if request.target not in valid_targets:
        raise HTTPException(
            status_code=400,
            detail=f"target은 {', '.join(valid_targets)} 중 하나여야 합니다."
        )

    # 세션 ID 생성 또는 재사용
    session_id = request.session_id or str(uuid.uuid4())

    # Service 인스턴스 생성
    service = TrainingService()

    # 톤 변환 평가
    result = service.evaluate_tone_conversion(
        session_id=session_id,
        original_sentence=request.original_sentence,
        user_modified_sentence=request.user_modified_sentence,
        target_tone=request.target_tone,
        target=request.target
    )

    return ToneConversionResponse(
        session_id=session_id,
        is_appropriate=result["is_appropriate"],
        feedback=result["feedback"],
        suggestions=result["suggestions"],
        example_sentence=result["example_sentence"],
        improvement_from_previous=result.get("improvement_from_previous", "")
    )


# ========== 세션 관리 엔드포인트 (선택적) ==========

@router.delete(
    "/session/{session_id}",
    summary="세션 삭제",
    description="훈련 세션을 삭제합니다. 세션 히스토리가 모두 삭제됩니다."
)
def delete_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    from repositories.session_memory import session_memory

    success = session_memory.clear_session(session_id)

    if success:
        return {
            "message": "세션이 삭제되었습니다.",
            "session_id": session_id
        }
    else:
        raise HTTPException(
            status_code=404,
            detail="세션을 찾을 수 없습니다."
        )


@router.get(
    "/session/{session_id}/history",
    summary="세션 히스토리 조회",
    description="특정 세션의 시도 히스토리를 조회합니다."
)
def get_session_history(
    session_id: str,
    last_n: int = 10,
    current_user: User = Depends(get_current_user)
):
    from repositories.session_memory import session_memory

    if not session_memory.session_exists(session_id):
        raise HTTPException(
            status_code=404,
            detail="세션을 찾을 수 없거나 만료되었습니다."
        )

    history = session_memory.get_history(session_id, last_n=last_n)
    total_turns = session_memory.get_turn_count(session_id)

    return {
        "session_id": session_id,
        "total_turns": total_turns,
        "history": history
    }
