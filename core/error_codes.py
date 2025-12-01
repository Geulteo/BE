from __future__ import annotations

from enum import Enum
from typing import Protocol
from fastapi import status


class BaseErrorCode(Protocol):
    @property
    def code(self) -> str:  # G001 같은 문자열 코드
        ...

    @property
    def message(self) -> str:  # 한글 메시지
        ...

    @property
    def http_status(self) -> int:  # fastapi.status.HTTP_... 상수
        ...


class GlobalErrorCode(Enum):
    # 공통
    INVALID_INPUT_VALUE = ("G001", "유효하지 않은 입력입니다.", status.HTTP_400_BAD_REQUEST)
    RESOURCE_NOT_FOUND = ("G002", "요청한 리소스를 찾을 수 없습니다.", status.HTTP_404_NOT_FOUND)
    INTERNAL_SERVER_ERROR = ("G003", "서버 내부 오류가 발생했습니다.", status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 인증 / 인가 관련
    UNAUTHORIZED = ("A001", "인증이 필요합니다. (JWT 토큰이 존재하지 않거나 유효하지 않습니다.)", status.HTTP_401_UNAUTHORIZED)
    FORBIDDEN = ("A002", "해당 리소스에 접근할 권한이 없습니다.", status.HTTP_403_FORBIDDEN)

    def __init__(self, code: str, message: str, http_status: int):
        self._code = code
        self._message = message
        self._http_status = http_status

    @property
    def code(self) -> str:
        return self._code

    @property
    def message(self) -> str:
        return self._message

    @property
    def http_status(self) -> int:
        return self._http_status
