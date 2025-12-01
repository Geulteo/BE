from __future__ import annotations

from typing import Optional

from .error_codes import BaseErrorCode


class CustomException(Exception):
    def __init__(self, error_code: BaseErrorCode, detail: Optional[str] = None):
        self.error_code = error_code
        # 별도 상세 메시지가 없으면 에러코드의 기본 메시지 사용
        self.detail = detail or error_code.message
        super().__init__(self.detail)
