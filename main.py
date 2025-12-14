from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from config.settings import get_settings

from database.session import Base, engine

import logging
from config.swagger_config import setup_swagger
from routers import auth, keyword, training_test, sentence, training
from repositories.user_sentence_repository import UserSentenceRepository
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from core.exception_handlers import register_exception_handlers
from services.difficulty_vector_store import DifficultyVectorStore
from services.difficulty_service import DifficultyService
from services.intent.classifier import IntentClassifier
from services.intent.pipeline import IntentPipeline
from services.intent.subtemplate_classifier import SubtemplateClassifier
from templates.difficulty_templates import DIFFICULTY_CARDS

logger = logging.getLogger(__name__)

settings = get_settings()

def get_cors_origins() -> list[str]:
    raw = settings.CORS_ORIGINS
    if not raw:
        return ["*"]
    raw = raw.strip()
    if raw == "*":
        return ["*"]
    # "http://localhost:3000, http://127.0.0.1:3000" 형태를 리스트로 변환
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


# FastAPI 실행 시, DB 자동 생성
@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    # 기존 테이블 삭제 (DB 테이블 구조 변경을 위한 테스트용)
    # print("DB 테이블 구조 변경 감지: 기존 테이블 삭제 중...")
    # Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)
    logger.info("DB 초기 테이블 생성 완료")

    # 난이도 진단 서비스 초기화 (RAG + Qdrant + SBERT)
    try:
        cards = DIFFICULTY_CARDS

        vector_store = DifficultyVectorStore(cards)
        difficulty_service = DifficultyService(vector_store)

        # 다른 곳(라우터)에서 DI로 꺼내 쓰기 위한 주입
        app_instance.state.difficulty_service = difficulty_service
        logger.info("난이도 진단 서비스 초기화 완료")
    except Exception as e:
        logger.exception(f"난이도 진단 서비스 초기화 중 오류 발생: {e}")

    # Intent 분류기 초기화
    try:
        classifier = IntentClassifier()
        pipeline = IntentPipeline(classifier)
        app_instance.state.intent_classifier = pipeline
        logger.info("Intent 분류기 초기화 완료")
        app_instance.state.subtemplate_classifier = SubtemplateClassifier(model=classifier.model)
        logger.info("Subtemplate 분류기 초기화 완료")

    except Exception as e:
        logger.exception(f"Intent 분류기 초기화 중 오류 발생: {e}")

    try:
        # SBERT 임베딩 모델 로드 (서버 시작 시 1회)
        embedder = SentenceTransformer(settings.SBERT_MODEL_NAME)
        app_instance.state.embedder = embedder
        logger.info("추천용 SBERT embedder 초기화 완료")

        # Qdrant client 초기화
        qdrant_client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )

        # 유저 문장 추천 Repository 생성
        user_sentence_repo = UserSentenceRepository(qdrant_client)

        # 추천용 컬렉션 없으면 생성
        user_sentence_repo.ensure_collection()

        # 다른 서비스/라우터에서 사용하도록 state 등록
        app_instance.state.user_sentence_repo = user_sentence_repo
        logger.info("유저 문장 추천 서비스 초기화 완료")

    except Exception as e:
        logger.exception(f"추천 기능 초기화 중 오류 발생: {e}")

    yield   # --- 앱이 실행되는 동안 --- #

    # shutdown
    logger.info("서버 종료")


app = FastAPI(
    lifespan=lifespan,
    # docs_url="/swagger-ui",
    # redoc_url="/redoc",
    # openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),  # .env에서 읽어온 origin 리스트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 예외 핸들러 등록
register_exception_handlers(app)

# Swagger
setup_swagger(app)

# auth 라우터
app.include_router(auth.router)
# keyword 라우터
app.include_router(keyword.router)

app.include_router(training_test.router)

app.include_router(sentence.router)   
app.include_router(training.router)