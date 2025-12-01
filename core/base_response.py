from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    code: str
    message: str
    data: Optional[Any] = None

    @classmethod
    def success_response(
        cls,
        data: Any = None,
        message: str = "요청이 성공적으로 처리되었습니다.",
    ) -> "BaseResponse":
        return cls(
            success=True,
            code="SUCCESS",
            message=message,
            data=data,
        )

    @classmethod
    def error_response(
        cls,
        code: str,
        message: str,
    ) -> "BaseResponse":
        return cls(
            success=False,
            code=code,
            message=message,
            data=None,
        )
