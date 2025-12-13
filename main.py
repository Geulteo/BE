from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from config.settings import get_settings

from database.session import Base, engine

import logging
from config.swagger_config import setup_swagger
from routers import auth, keyword, training_test
from core.exception_handlers import register_exception_handlers
from repositories.difficulty_repository import DifficultyCardRepository
from services.difficulty_vector_store import DifficultyVectorStore
from services.difficulty_service import DifficultyService
from services.intent.classifier import IntentClassifier
from services.intent.pipeline import IntentPipeline
from services.intent.subtemplate_classifier import SubtemplateClassifier

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
        repo = DifficultyCardRepository("./data/difficulty_cards.json")
        cards = repo.load_all()

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