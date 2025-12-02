from fastapi import APIRouter, Depends
from core.base_response import BaseResponse
from models.keyword import KeywordRequest
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
    response_model=BaseResponse,
)
def handle_user_input(
        data: KeywordRequest,
        current_user: dict = Depends(get_current_user)
) -> BaseResponse:

    user_id = current_user.get("sub")
    result = keyword_service.process_user_input(data, user_id=user_id)

    #키워드 부족 검증 결과 확인
    if result.get("error") is True:
        raise CustomException(
            GlobalErrorCode.INVALID_INPUT_VALUE,
            detail=result["message"]
        )

    # 성공 결과 반환
    response_data = {
        k: v for k, v in result.items()
        if k not in ["error", "message"]
    }

    return BaseResponse.success_response(
        data=response_data,
        message="키워드 전처리 및 검증 완료"
    )