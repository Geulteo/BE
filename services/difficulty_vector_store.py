from typing import List, Dict, Any
import uuid

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

from models.difficulty_card import DifficultyCard
from core.level_enums import DifficultyLevel
from config.settings import get_settings

settings = get_settings()


class DifficultyVectorStore:
    # 난이도 기준 카드를 Qdrant에 인덱싱하고 검색하는 클래스
    def __init__(
        self,
        cards: List[DifficultyCard],
        client: QdrantClient | None = None,
    ):
        self.cards = cards
        self.collection_name = settings.QDRANT_DIFFICULTY_COLLECTION

        # SBERT 모델은 싱글톤처럼 사용 (배포 시 성능 고려)
        self.model = SentenceTransformer(settings.SBERT_MODEL_NAME)

        # Qdrant 클라이언트 (Docker / 배포 환경에서 host, port 주입)
        self.client = client or QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )

        self._create_collection_if_needed()
        self._index_cards()

    def _create_collection_if_needed(self) -> None:
        # 컬렉션이 없으면 생성, 있으면 그대로 사용
        collections = [c.name for c in self.client.get_collections().collections]
        if self.collection_name in collections:
            return

        # SBERT 768차원 기준, 코사인 거리 사용
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

    def _index_cards(self) -> None:
        # 난이도 기준 카드 전체를 Qdrant에 upsert
        points: List[PointStruct] = []

        for card in self.cards:
            doc = card.to_prompt_text()
            embedding = self.model.encode(doc).tolist()

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "intent": card.intent.value,
                        "template_id": card.template_id.value,
                        "target": card.target,
                        "level": card.level.value,
                        "document": doc,
                    },
                )
            )

        if points:
            self.client.upsert(collection_name=self.collection_name, points=points)

    def search_cards(
            self,
            query_text: str,
            top_k: int = 5,
            level: DifficultyLevel | None = None,
            target: str | None = None,
            intent: str | None = None,  # 이미 추가했을 수도 있음
            template_id: str | None = None,  # 🔹 template_id도 받기
    ):
        # 1) 쿼리 문장 임베딩
        query_vector = self.model.encode(query_text).tolist()

        # 2) 필터 조건 구성
        must_conditions: list[FieldCondition] = []

        if level is not None:
            must_conditions.append(
                FieldCondition(
                    key="level",
                    match=MatchValue(value=level.value),
                )
            )

        if target is not None:
            must_conditions.append(
                FieldCondition(
                    key="target",
                    match=MatchValue(value=target),
                )
            )

        if intent is not None:
            must_conditions.append(
                FieldCondition(
                    key="intent",
                    match=MatchValue(value=intent),
                )
            )

        if template_id is not None:
            must_conditions.append(
                FieldCondition(
                    key="template_id",  # 🔹 Qdrant payload의 키 이름과 맞춰야 함
                    match=MatchValue(value=template_id),
                )
            )

        qdrant_filter = Filter(must=must_conditions) if must_conditions else None

        result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=qdrant_filter,
            limit=top_k,
            with_payload=True,
        )

        return result