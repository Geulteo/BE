from __future__ import annotations

import logging

from fastapi import FastAPI, Request
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

        response_body = BaseResponse.failure(
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

        response_body = BaseResponse.failure(
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

        response_body = BaseResponse.failure(
            code=GlobalErrorCode.INTERNAL_SERVER_ERROR.code,
            message=GlobalErrorCode.INTERNAL_SERVER_ERROR.message,
        )

        return JSONResponse(
            status_code=GlobalErrorCode.INTERNAL_SERVER_ERROR.http_status,
            content=response_body.model_dump(),
        )
