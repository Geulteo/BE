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

def get_subtemplate_classifier(request: Request):
    return request.app.state.subtemplate_classifier


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
        subtemplate_classifier=Depends(get_subtemplate_classifier),
) -> BaseResponse:

    user_id = current_user.get("sub")

    # 1) 키워드 전처리 서비스 실행
    result = keyword_service.process_user_input(data, user_id=user_id)

    if result.get("error"):
        return BaseResponse.error_response(
            code="G001",
            message=result["message"],
        )

    # SBERT 입력 문장 확보 (전처리 결과에 없을 수도 있어서 fallback 처리)
    fallback_sentence_for_sbert = (
        result.get("sentence_for_sbert")
        or result.get("sbert_sentence")
        or result.get("cleaned_text")
        or ""
    )

    sentence_for_sbert = fallback_sentence_for_sbert

    # 2) Intent 분류 실행 (Pipeline.run)
    try:
        intent_result = intent_classifier.run(data)

    except Exception as e:
        print("Intent Classification Error:", e)
        return BaseResponse.error_response(
            code="G003",
            message="의도 분석 중 문제가 발생했습니다.",
        )

    intent_label = intent_result.intent  # Enum
    model_sentence = intent_result.sentence_for_sbert  # str

    if model_sentence:
        sentence_for_sbert = model_sentence

    # Enum -> "request"
    if hasattr(intent_label, "value"):
        intent_label = intent_label.value

    # Subtemplate(세부 템플릿) 추천 실행
    structure_template = None
    try:
        if intent_label and sentence_for_sbert:
            structure_template = subtemplate_classifier.classify(
                intent=str(intent_label).upper(),
                sentence_for_sbert=sentence_for_sbert,
            )

    except Exception as e:
        structure_template = None

    # 3) 최종 응답 데이터 구성
    response_data = {
        "cleaned_text": result.get("cleaned_text"),
        "keywords": result.get("keywords"),
        "pos_tags": result.get("pos_tags"),
        "tone": result.get("tone"),
        "length_option": result.get("length_option"),
        "target": result.get("target"),
        "sentence_for_sbert": sentence_for_sbert,
        "intent_prediction": intent_result,
        "structure_template": structure_template,
    }

    return BaseResponse.success_response(
        data=response_data,
        message="키워드 전처리 및 Intent/구조 템플릿 추천 완료",
    )