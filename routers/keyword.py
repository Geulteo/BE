from fastapi import APIRouter, Depends, Request
from core.base_response import BaseResponse
from models.keyword import KeywordRequest
from services import keyword as keyword_service
from services.sentence_generator import SentenceGeneratorService
from services.recommendation_service import RecommendationService
from config.swagger_config import get_current_user
import traceback

router = APIRouter(
    prefix="/keyword",
    tags=["Keyword"],
)

# Intent Classifier DI
def get_intent_classifier(request: Request):
    return request.app.state.intent_classifier

def get_subtemplate_classifier(request: Request):
    return request.app.state.subtemplate_classifier

def get_recommendation_service(request: Request) -> RecommendationService:  # 수정
    return RecommendationService(
        repo=request.app.state.user_sentence_repo,
        embedder=request.app.state.embedder,
    )


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
        current_user: dict = Depends(get_current_user),
        intent_classifier=Depends(get_intent_classifier),
        subtemplate_classifier=Depends(get_subtemplate_classifier),
        rec_svc: RecommendationService = Depends(get_recommendation_service),
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

        # =========================
        # 5) 여기서 문장 생성까지 연결
        # =========================

        # 5-1) 문장 생성 입력값 준비
    keywords = result.get("keywords") or []
    tone = result.get("tone")
    length_option = result.get("length_option")
    target = result.get("target")

    # 5-2) structure_template에서 template_id / template_slots 안전 추출
    template_id = None
    template_slots = None

    if isinstance(structure_template, dict):
        template_id = (
            structure_template.get("template_id")
            or structure_template.get("template_name")   #  template_name을 template_id로 사용
            or structure_template.get("id")
        )
        template_slots = (
            structure_template.get("template_slots")
            or structure_template.get("slot_list")       #  slot_list를 slots로 사용
            or structure_template.get("slots")
        )
    else:
        if structure_template is not None:
            template_id = (
                getattr(structure_template, "template_id", None)
                or getattr(structure_template, "template_name", None)
                or getattr(structure_template, "id", None)
            )
            template_slots = (
                getattr(structure_template, "template_slots", None)
                or getattr(structure_template, "slot_list", None)
                or getattr(structure_template, "slots", None)
            )

    print("[GEN INPUT]", {  # 버깅 로그
        "keywords": keywords,
        "intent": intent_label,
        "template_id": template_id,
        "template_slots": template_slots,
        "tone": tone,
        "length_option": length_option,
        "target": target,
    })

    generated_sentence = None
    generation_error = None  # null 뜨는 원인(예외)을 응답에 같이 넣기



    # 5-4) SentenceGeneratorService로 최종 문장 생성
    try:
        service = SentenceGeneratorService()
        generated_sentence = service.generate_sentence(
            keywords=keywords,
            intent=intent_label,
            template_id=template_id,
            template_slots=template_slots,
            tone=tone,
            length_option=length_option,
            target=target,
        )

        # 혹시 dict 형태로 반환하는 구현이면 문자열만 뽑아오기
        if isinstance(generated_sentence, dict):
            generated_sentence = generated_sentence.get("generated_sentence")

        # 결과가 빈 문자열/None이면 원인 파악을 돕기 위해 에러 메시지 세팅
        if not generated_sentence:
            generation_error = "generate_sentence returned empty result (None or '')."

    except Exception as e:
        generation_error = str(e)
        print("Sentence Generation Error:", e)
        print(traceback.format_exc())  # 어떤 줄에서 터졌는지 전부 출력
        generated_sentence = None

        # =========================
        # 5) generated_sentence 기반 Top3 추천 추가  # 수정
        # =========================
    recommendations_top3 = []
    recommendation_error = None

    try:
        if user_id is not None and generated_sentence:
            recommendations_top3 = rec_svc.recommend(
                user_id=user_id,
                text=generated_sentence,
                intent=intent_label,
                target=target,
                template_id=template_id,
            )

            # (원하면) 지금 생성된 문장을 히스토리로 저장
            rec_svc.save(
                user_id=user_id,
                text=generated_sentence,
                payload={
                    "intent": intent_label,
                    "target": target,
                    "template_id": template_id,
                },
            )
    except Exception as e:
        recommendation_error = str(e)
        print("Recommendation Error:", e)
        print(traceback.format_exc())
        recommendations_top3 = []

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
        "generated_sentence": generated_sentence,
        "generation_meta": {
            "intent_used": intent_label,
            "template_id_used": template_id,
            "tone_used": tone,
            "length_used": length_option,
            "target_used": target,
        },
        "generation_error": generation_error,

        "recommendations_top3": recommendations_top3,  # 수정
        "recommendation_error": recommendation_error,  # 수정
    }

    return BaseResponse.success_response(
        data=response_data,
        message="키워드 전처리 및 Intent/구조 템플릿 추천 완료",
    )