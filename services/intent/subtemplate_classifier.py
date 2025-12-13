from typing import Dict, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

from templates.structure_templates import SUBTEMPLATES, SLOT_BY_INTENT
from models.structure_template import StructureTemplateResult


class SubtemplateClassifier:
    # intent 안에서 세부 템플릿(template_name)을 SBERT 유사도로 선택하고, 해당 intent의 slot_list를 함께 반환

    def __init__(self, model: SentenceTransformer):
        self.model = model
        self._index: Dict[str, Dict] = {}

        # ▶ 템플릿 설명문 임베딩: 초기화 시 1회
        for intent, template_map in SUBTEMPLATES.items():
            template_names = list(template_map.keys())
            descriptions = list(template_map.values())

            embeddings = self.model.encode(
                descriptions,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False,
            )

            self._index[intent] = {
                "template_names": template_names,
                "embeddings": embeddings,
            }

    def classify(
        self,
        intent: str,
        sentence_for_sbert: str,
    ) -> Optional[StructureTemplateResult]:

        intent = intent.upper().strip()
        if intent not in self._index:
            return None

        query_emb = self.model.encode(
            sentence_for_sbert,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        sims = self._index[intent]["embeddings"] @ query_emb
        best_idx = int(np.argmax(sims))

        template_name = self._index[intent]["template_names"][best_idx]
        slot_list = SLOT_BY_INTENT[intent]

        return StructureTemplateResult(
            template_name=template_name,
            slot_list=slot_list,
            score=float(sims[best_idx]),
        )
