from __future__ import annotations

from services.intent.classifier import IntentClassifier
from models.intent import IntentResult
from services.preprocess import preprocess_and_validate_input

# 전처리 + IntentClassifier 묶는 서비스
class IntentPipeline:

    def __init__(self, classifier: IntentClassifier):
        self.classifier = classifier

    def run(self, user_text_obj) -> IntentResult:

        # 1) 전처리 호출
        pre = preprocess_and_validate_input(user_text_obj)

        if pre.get("error"):
            return IntentResult(
                cleaned_text=pre["cleaned_text"],
                keywords=pre["keywords"],
                pos_tags=pre["pos_tags"],
                sentence_for_sbert=pre["sentence_for_sbert"],
                intent=None,
                intent_scores={},
                need_more_info=True,
                need_more_info_message=pre["message"],
            )

        # 2) IntentClassifier 호출
        result = self.classifier.classify(
            sentence=pre["sentence_for_sbert"],
            keywords=pre["keywords"],
        )

        # 3) Pydantic 모델에 매핑
        return IntentResult(
            cleaned_text=pre["cleaned_text"],
            keywords=pre["keywords"],
            pos_tags=pre["pos_tags"],
            sentence_for_sbert=pre["sentence_for_sbert"],
            intent=result["predicted_intent"],
            intent_scores={k.value: float(v) for k, v in result["scores"].items()},
            need_more_info=result["need_more_info"],
            need_more_info_message=(
                "조금 더 구체적으로 입력해주세요." if result["need_more_info"] else None
            ),
        )