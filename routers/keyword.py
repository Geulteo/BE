from fastapi import APIRouter, Depends, Request
from core.base_response import BaseResponse
from models.keyword import KeywordRequest
from services import keyword as keyword_service
from services.sentence_generator import SentenceGeneratorService
from services.recommendation_service import RecommendationService
from config.swagger_config import get_current_user
import traceback

import logging
from typing import Any, Dict, List, Optional, Tuple

from services.keyword_helpers import (
    ensure_str_intent,
    pick_sentence_for_sbert,
    extract_template_info,
    to_jsonable,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/keyword",
    tags=["Keyword"],
)

# Intent Classifier DI
def get_intent_classifier(request: Request):
    return request.app.state.intent_classifier

def get_subtemplate_classifier(request: Request):
    return request.app.state.subtemplate_classifier

def get_recommendation_service(request: Request) -> RecommendationService:
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
        request: Request,
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
            message=result.get("message", "전처리 중 오류가 발생했습니다."),
        )

    sentence_for_sbert = pick_sentence_for_sbert(result)

    # 2) Intent 분류 실행 (Pipeline.run)
    try:
        intent_result = intent_classifier.run(data)

    except Exception as e:
        logger.exception("Intent Classification Error: %s", e)
        return BaseResponse.error_response(
            code="G003",
            message="의도 분석 중 문제가 발생했습니다.",
        )

    # Enum/str 안전 정규화
    intent_label = ensure_str_intent(getattr(intent_result, "intent", None))
    model_sentence = getattr(intent_result, "sentence_for_sbert", None)

    if model_sentence:
        sentence_for_sbert = model_sentence

    # 3) Subtemplate(세부 템플릿) 추천 실행
    structure_template = None
    try:
        if intent_label and sentence_for_sbert:
            structure_template = subtemplate_classifier.classify(
                intent=str(intent_label).upper(),
                sentence_for_sbert=sentence_for_sbert,
            )

    except Exception as e:
        logger.warning("Subtemplate classify failed: %s", e)  # 수정
        structure_template = None

    # 4) 문장 생성 입력값 준비
    keywords = result.get("keywords") or []
    tone = result.get("tone")
    length_option = result.get("length_option")
    target = result.get("target")

    template_id, template_slots = extract_template_info(structure_template)

    logger.info("[GEN INPUT] %s", {
        "keywords": keywords,
        "intent": intent_label,
        "template_id": template_id,
        "template_slots": template_slots,
        "tone": tone,
        "length_option": length_option,
        "target": target,
    })

    generated_sentence = None
    generation_error = None

    # 5) SentenceGeneratorService로 최종 문장 생성
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
        logger.error("Sentence Generation Error: %s", e)
        logger.debug(traceback.format_exc())
        generated_sentence = None

    # 6) generated_sentence 기반 Top3 추천
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

            # 지금 생성된 문장을 히스토리로 저장
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
        logger.error("Recommendation Error: %s", e)
        logger.debug(traceback.format_exc())
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
        "intent_prediction": to_jsonable(intent_result),
        "structure_template": to_jsonable(structure_template),
        "generated_sentence": generated_sentence,
        "generation_meta": {
            "intent_used": intent_label,
            "template_id_used": template_id,
            "tone_used": tone,
            "length_used": length_option,
            "target_used": target,
        },
        "generation_error": generation_error,

        "recommendations_top3": to_jsonable(recommendations_top3),
        "recommendation_error": recommendation_error,
    }

    return BaseResponse.success_response(
        data=response_data,
        message="키워드 전처리 및 Intent/구조 템플릿 추천 완료",
    )