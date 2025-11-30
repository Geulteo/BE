from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.session import Base, engine

import logging

import models.user
from routers import auth, keyword

logger = logging.getLogger(__name__)

# FastAPI 실행 시, DB 자동 생성
@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    # 기존 테이블 삭제 (DB 테이블 구조 변경을 위한 테스트용)
    # print("DB 테이블 구조 변경 감지: 기존 테이블 삭제 중...")
    # Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)
    logger.info("DB 초기 테이블 생성 완료")

    yield   # --- 앱이 실행되는 동안 --- #

    # shutdown
    logger.info("서버 종료")

app = FastAPI(lifespan=lifespan)
# auth 라우터
app.include_router(auth.router)
# keyword 라우터
app.include_router(keyword.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
