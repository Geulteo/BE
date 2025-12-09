from fastapi import APIRouter, Depends, Request
from core.base_response import BaseResponse
from models.keyword import KeywordRequest
from services import keyword as keyword_service
from config.swagger_config import get_current_user

router = APIRouter(
    prefix="/keyword",
    tags=["Keyword"],
)

# Intent Classifier DI
def get_intent_classifier(request: Request):
    return request.app.state.intent_classifier


@router.post(
    "/preprocess",
    response_model=BaseResponse,
    summary="사용자 키워드 전처리 및 검증",
    description=(
        "사용자가 입력한 텍스트를 정제하고 키워드를 추출한 뒤, "
        "문장이면 그대로, 키워드만 있으면 LLM 기반 문장 복원 후 Intent를 추론합니다."
    ),
)
def handle_user_input(
        data: KeywordRequest,
        request: Request,
        current_user: dict = Depends(get_current_user),
        intent_classifier=Depends(get_intent_classifier),
) -> BaseResponse:

    user_id = current_user.get("sub")

    # 1) 키워드 전처리 서비스 실행
    result = keyword_service.process_user_input(data, user_id=user_id)

    if result.get("error"):
        return BaseResponse.error_response(
            code="G001",
            message=result["message"],
        )


    # 2) Intent 분류 실행
    raw_text = result.get("cleaned_text", "")
    keywords = result.get("keywords", [])

    try:
        intent_result = intent_classifier.predict(
            raw_text=raw_text,
            keywords=keywords  # 문장이면 내부에서 무시
        )
    except Exception as e:
        print("Intent Classification Error:", e)
        return BaseResponse.error_response(
            code="G003",
            message="의도 분석 중 문제가 발생했습니다.",
        )

    # 3) 최종 응답 데이터 구성
    response_data = {
        "cleaned_text": raw_text,
        "keywords": keywords,
        "pos_tags": result.get("pos_tags"),
        "tone": result.get("tone"),
        "length_option": result.get("length_option"),
        "target": result.get("target"),
        "intent_prediction": intent_result,
    }

    return BaseResponse.success_response(
        data=response_data,
        message="키워드 전처리 및 Intent 추론 완료",
    )
