from typing import Any

from fastapi import APIRouter, Depends, Request

from models.difficulty_request import DifficultyDiagnosisRequest
from models.difficulty_response import DifficultyDiagnosisResult
from services.difficulty_service import DifficultyService
from core.base_response import BaseResponse

from services.auth import get_current_user
from services.preprocess import preprocess_and_validate_input
from services.preprocess import build_sentence_for_sbert

router = APIRouter(
    prefix="/training",
    tags=["Training"],
)

# difficulty_service 인스턴스를 가져오는 함수
def get_difficulty_service(request: Request) -> DifficultyService:
    return request.app.state.difficulty_service

# 연습 난이도 진단
@router.post(
    "/difficulty/diagnose",
    response_model=BaseResponse,
    summary="훈련 난이도 진단 (RAG 기반)",
)
async def diagnose_difficulty(
    body: DifficultyDiagnosisRequest,
    current_user: Any = Depends(get_current_user),
    service: DifficultyService = Depends(get_difficulty_service),
) -> BaseResponse:

    # 1) 문장 전처리 → sentence_for_sbert 생성
    sentence_for_sbert = build_sentence_for_sbert(body.user_sentence)

    # 2) 사용자 ID 추출 (User 객체 기준)
    user_id = getattr(current_user, "id", None)

    result: DifficultyDiagnosisResult = service.diagnose_difficulty(
        user_sentence=body.user_sentence,
        sentence_for_sbert=sentence_for_sbert,
        intent=body.intent.value,
        template_id=body.template_id.value,
        target=body.target,
        user_id=user_id,
    )

    return BaseResponse.success_response(
        data=result,
        message="난이도 진단이 완료되었습니다.",
    )
