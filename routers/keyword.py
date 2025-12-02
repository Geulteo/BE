from fastapi import APIRouter, status, Depends
from typing import Dict, Any

from models.keyword import KeywordRequest, PreprocessResult
from services import keyword as keyword_service

from config.swagger_config import  get_current_user
from core.exceptions import CustomException
from core.error_codes import GlobalErrorCode

router = APIRouter(
    prefix="/keyword",
    tags=["Keyword"],
)

# 입력 검증 및 전처리 (POST/keyword/preprocess)
@router.post(
    "/preprocess",
    response_model=PreprocessResult,
    summary="Keyword preprocessing",
    tags=["Keyword"],
    responses={
        400: {"description": "키워드 부족 안내"}
    }
)
def handle_user_input(
        data: KeywordRequest,
        current_user: dict = Depends(get_current_user)
) -> PreprocessResult:

    result = keyword_service.process_user_input(data)

    #키워드 부족 검증 결과 확인
    if result["error"]:
        raise CustomException(
            GlobalErrorCode.INVALID_INPUT_VALUE,
            detail=result["message"]
        )

    # 성공 결과 반환
    return result["data"]