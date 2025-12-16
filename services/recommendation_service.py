from __future__ import annotations

from typing import Any, Dict, List, Optional

from repositories.user_sentence_repository import UserSentenceRepository

# 추천(유사 문장 검색) : 3단계 fallback
class RecommendationService:
    TOP_K: int = 3
    SCORE_THRESHOLD: float = 0.80

    # Repository(Qdrant 접근)와 Embedder(SBERT)를 주입받아 추천/저장 로직을 수행할 준비를 한다.
    def __init__(self, repo: UserSentenceRepository, embedder):
        self.repo = repo
        self.embedder = embedder

    # 입력 문장을 SBERT로 임베딩한 뒤 Qdrant에 넣을 수 있는 float 리스트로 변환한다.
    def _embed(self, text: str) -> List[float]:
        vec = self.embedder.encode([text], normalize_embeddings=True)[0]
        return vec.tolist()

    # fallback 단계에서 중복 추천이 생길 수 있어 text 기준으로 중복을 제거하고 우선순위를 유지한다.
    def _dedup_by_text(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        out: List[Dict[str, Any]] = []
        for it in items:
            t = (it.get("text") or "").strip()
            if not t or t in seen:
                continue
            seen.add(t)
            out.append(it)
        return out

    # (1)엄격→(2)완화→(3)최후(user_id만) 순서로 검색하여 Top3 추천
    def recommend(
        self,
        *,
        user_id: int,
        text: str,
        intent: Optional[str] = None,
        target: Optional[str] = None,
        template_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        query_vec = self._embed(text)
        collected: List[Dict[str, Any]] = []

        # 1) user_id + intent + target + template_id
        if intent is not None and target is not None and template_id is not None:
            res1 = self.repo.search_similar(
                user_id=user_id,
                query_vector=query_vec,
                limit=self.TOP_K,
                score_threshold=self.SCORE_THRESHOLD,
                intent=intent,
                target=target,
                template_id=template_id,
            )
            collected.extend(res1)

        collected = self._dedup_by_text(collected)
        if len(collected) >= self.TOP_K:
            return collected[: self.TOP_K]

        # 2) user_id + intent + target
        if intent is not None and target is not None:
            res2 = self.repo.search_similar(
                user_id=user_id,
                query_vector=query_vec,
                limit=self.TOP_K,
                score_threshold=self.SCORE_THRESHOLD,
                intent=intent,
                target=target,
                template_id=None,
            )
            collected.extend(res2)

        collected = self._dedup_by_text(collected)
        if len(collected) >= self.TOP_K:
            return collected[: self.TOP_K]

        # 3) user_id only
        res3 = self.repo.search_similar(
            user_id=user_id,
            query_vector=query_vec,
            limit=self.TOP_K,
            score_threshold=self.SCORE_THRESHOLD,
            intent=None,
            target=None,
            template_id=None,
        )
        collected.extend(res3)

        collected = self._dedup_by_text(collected)
        return collected[: self.TOP_K]

    def save(
        self,
        *,
        user_id: int,
        text: str,
        payload: Dict[str, Any],
    ) -> str:
        vec = self._embed(text)
        return self.repo.upsert_sentence(
            user_id=user_id,
            text=text,
            vector=vec,
            payload=payload,
        )
