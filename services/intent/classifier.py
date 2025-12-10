from __future__ import annotations
import numpy as np
from typing import Dict, List
from sentence_transformers import SentenceTransformer

from services.intent.config import (
    INTENT_TEMPLATES,
    INTENT_KEYWORD_BOOST,
    INTENT_KEYWORD_WEIGHT,
    TOP_K,
    TOP_THRESHOLD,
    DIFF_THRESHOLD,
)
from core.type_enums import IntentType
from config.settings import get_settings

settings = get_settings()


class IntentClassifier:
    """SBERT 기반 Intent Classification"""

    def __init__(self, model: SentenceTransformer | None = None):
        self.model = model or SentenceTransformer(settings.SBERT_MODEL_NAME)
        self.top_k = TOP_K

        # 템플릿 → 벡터 사전 생성
        self.template_texts = []
        self.template_labels = []

        for intent, examples in INTENT_TEMPLATES.items():
            for s in examples:
                self.template_texts.append(s)
                self.template_labels.append(intent)

        self.template_embeddings = self.model.encode(
            self.template_texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    # SBERT Top-k 평균 계산
    def _compute_sbert_scores(self, sentence: str) -> Dict[IntentType, float]:
        q = self.model.encode(sentence, convert_to_numpy=True, normalize_embeddings=True)
        sims = self.template_embeddings @ q

        grouped = {intent: [] for intent in INTENT_TEMPLATES}
        for idx, sim in enumerate(sims):
            grouped[self.template_labels[idx]].append(float(sim))

        scores = {}
        for intent, vals in grouped.items():
            scores[intent] = float(np.mean(sorted(vals, reverse=True)[: self.top_k]))

        return scores

    # Keyword 기반 Rule boost
    def _compute_rule_boost(self, keywords: List[str]) -> Dict[IntentType, float]:
        joined_kw = " ".join(keywords)
        boost = {intent: 0.0 for intent in INTENT_TEMPLATES}

        for intent, kw_list in INTENT_KEYWORD_BOOST.items():
            if any(k in joined_kw for k in kw_list):
                boost[intent] += INTENT_KEYWORD_WEIGHT[intent]

        return boost

    # 최종 Intent 결정
    def classify(self, sentence: str, keywords: List[str] | None = None) -> Dict:
        keywords = keywords or []

        sbert_scores = self._compute_sbert_scores(sentence)
        boost_scores = self._compute_rule_boost(keywords)

        final_scores = {
            intent: sbert_scores[intent] + boost_scores[intent]
            for intent in sbert_scores
        }

        ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        top_intent, top_score = ranked[0]
        second_score = ranked[1][1]

        need_more_info = (
            top_score < TOP_THRESHOLD
            or (top_score - second_score) < DIFF_THRESHOLD
        )

        return {
            "sentence_used": sentence,
            "predicted_intent": top_intent,
            "scores": final_scores,
            "need_more_info": need_more_info,
        }