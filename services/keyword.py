from typing import Dict, Any
from models.keyword import KeywordRequest
from services.preprocess import preprocess_and_validate_input

def process_user_input(request: KeywordRequest, user_id: str) -> Dict[str, Any]:

    # 전처리 및 검증
    result: Dict[str, Any] = preprocess_and_validate_input(request)

    # 키워드 부족 시 오류 응답 (Dict) 반환
    if result.get("error", False) is True:
        # 오류 메시지와 전처리 데이터를 포함하는 Dict를 즉시 반환합니다.
        return result

    return result