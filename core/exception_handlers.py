from __future__ import annotations

import logging

from fastapi import FastAPI, Request,HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .exceptions import CustomException
from .error_codes import GlobalErrorCode
from .base_response import BaseResponse

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    # 1. 커스텀 예외 처리
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        error_code = exc.error_code

        logger.warning(
            "CustomException 발생: %s %s | code=%s message=%s",
            request.method,
            request.url,
            error_code.code,
            exc.detail,
        )

        response_body = BaseResponse.error_response(
            code=error_code.code,
            message=exc.detail,  # detail 없으면 error_code.message 가 들어 있음
        )

        return JSONResponse(
            status_code=error_code.http_status,
            content=response_body.model_dump(),
        )

    # 2. FastAPI / Pydantic Request Validation 오류
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        # 필드별 에러 메시지 정리
        error_messages = []
        for err in exc.errors():
            loc = " -> ".join(str(x) for x in err.get("loc", []))
            msg = err.get("msg", "")
            error_messages.append(f"{loc}: {msg}")

        joined_message = "; ".join(error_messages) if error_messages else GlobalErrorCode.INVALID_INPUT_VALUE.message

        logger.info(
            "RequestValidationError: %s %s | errors=%s",
            request.method,
            request.url,
            joined_message,
        )

        response_body = BaseResponse.error_response(
            code=GlobalErrorCode.INVALID_INPUT_VALUE.code,
            message=joined_message,
        )

        return JSONResponse(
            status_code=GlobalErrorCode.INVALID_INPUT_VALUE.http_status,
            content=response_body.model_dump(),
        )

    # 3. 예상치 못한 모든 예외
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error("Server 오류 발생: %s %s", request.method, request.url, exc_info=exc)

        response_body = BaseResponse.error_response(
            code=GlobalErrorCode.INTERNAL_SERVER_ERROR.code,
            message=GlobalErrorCode.INTERNAL_SERVER_ERROR.message,
        )

        return JSONResponse(
            status_code=GlobalErrorCode.INTERNAL_SERVER_ERROR.http_status,
            content=response_body.model_dump(),
        )

    # FastAPI가 던지는 기본 HTTPException (특히 401/403)을 처리
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        # 기본값 설정
        error_code = GlobalErrorCode.INTERNAL_SERVER_ERROR
        http_status = exc.status_code

        # FastAPI/HTTPBearer가 던지는 기본 영어 메시지들
        DEFAULT_401_MESSAGES = ["Unauthorized", "Not authenticated", "Not Authorized"]
        DEFAULT_403_MESSAGES = ["Forbidden", "Not permitted"]

        # detail_message 초기값 설정
        detail_message = exc.detail

        # 401 Unauthorized 처리
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            error_code = GlobalErrorCode.UNAUTHORIZED
            # 기본 영어 메시지 중 하나라면, 한국어 메시지로 강제 치환
            if exc.detail in DEFAULT_401_MESSAGES:
                detail_message = error_code.message  # GlobalErrorCode의 한국어 메시지
            else:
                detail_message = exc.detail  # 사용자 정의된 detail은 유지 (로그인 실패 등)

        # 403 Forbidden 처리
        elif exc.status_code == status.HTTP_403_FORBIDDEN:
            error_code = GlobalErrorCode.FORBIDDEN
            if exc.detail in DEFAULT_403_MESSAGES:
                detail_message = error_code.message
            else:
                detail_message = exc.detail

        # 그 외 HTTPException 처리
        elif exc.status_code == status.HTTP_404_NOT_FOUND:
            error_code = GlobalErrorCode.RESOURCE_NOT_FOUND
            detail_message = error_code.message

        logger.warning(
            "HTTPException 발생: %s %s | code=%s message=%s",
            request.method,
            request.url,
            error_code.code,
            detail_message,
        )

        response_body = BaseResponse.error_response(
            code=error_code.code,
            message=detail_message,
        )

        return JSONResponse(
            status_code=exc.status_code,  # 원래의 HTTP 상태 코드를 유지
            content=response_body.model_dump(),
        )
