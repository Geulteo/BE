from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.session import Base, engine

import logging

import models.user
from routers import auth

logger = logging.getLogger(__name__)

# FastAPI 실행 시, DB 자동 생성
@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("DB 초기 테이블 생성 완료")

    yield   # --- 앱이 실행되는 동안 --- #

    # shutdown
    logger.info("서버 종료")

app = FastAPI(lifespan=lifespan)
# auth 라우터
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
