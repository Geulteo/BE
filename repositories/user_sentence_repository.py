from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
    PointStruct,
)

from config.settings import get_settings

settings = get_settings()

# Qdrant에 user 문장(원문 + 임베딩 + 메타데이터)을 저장하고, 유사 문장을 검색하는 Repository
class UserSentenceRepository:
    def __init__(self, client: QdrantClient):
        self.client = client
        self.collection = settings.QDRANT_USER_SENTENCE_COLLECTION

    # 추천용 컬렉션이 없으면 SBERT_DIM과 COSINE 거리 기준으로 새로 생성
    def ensure_collection(self) -> None:
        collections = self.client.get_collections()
        names = {c.name for c in collections.collections}

        if self.collection in names:
            return

        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(
                size=settings.SBERT_DIM,
                distance=Distance.COSINE,
            ),
        )

    # 한줄: 사용자 문장과 임베딩 벡터 및 메타데이터(payload)를 Qdrant에 1건 저장(upsert)한다.
    def upsert_sentence(
        self,
        *,
        user_id: int,
        text: str,
        vector: List[float],
        payload: Dict[str, Any],
    ) -> str:
        point_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        merged_payload = {
            "user_id": user_id,
            "text": text,
            "created_at": payload.get("created_at") or now_iso,
            **payload,
        }

        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=merged_payload,
                )
            ],
        )
        return point_id

    # 한줄: user_id(필수)와 선택 필터(intent/target/template_id)로 범위를 제한한 뒤 유사 문장을 검색한다.
    def search_similar(
        self,
        *,
        user_id: int,
        query_vector: List[float],
        limit: int,
        score_threshold: float,
        intent: Optional[str] = None,
        target: Optional[str] = None,
        template_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        must_conditions = [
            FieldCondition(key="user_id", match=MatchValue(value=user_id)),
        ]

        if intent is not None:
            must_conditions.append(
                FieldCondition(key="intent", match=MatchValue(value=intent))
            )
        if target is not None:
            must_conditions.append(
                FieldCondition(key="target", match=MatchValue(value=target))
            )
        if template_id is not None:
            must_conditions.append(
                FieldCondition(key="template_id", match=MatchValue(value=template_id))
            )

        flt = Filter(must=must_conditions)

        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            query_filter=flt,
            limit=limit,
            score_threshold=score_threshold,
            with_payload=True,
        )

        items: List[Dict[str, Any]] = []
        for r in results:
            payload = r.payload or {}
            items.append(
                {
                    "text": payload.get("text", ""),
                    "score": float(r.score),
                    "created_at": payload.get("created_at"),
                    "intent": payload.get("intent"),
                    "target": payload.get("target"),
                    "template_id": payload.get("template_id"),
                }
            )
        return items
