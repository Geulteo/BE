from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.session import Base, engine

import logging
from config.swagger_config import setup_swagger

import models.user
from routers import auth, keyword

from core.exception_handlers import register_exception_handlers

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

# 전역 예외 핸들러 등록
register_exception_handlers(app)

# Swagger
setup_swagger(app)

# auth 라우터
app.include_router(auth.router)
# keyword 라우터
app.include_router(keyword.router)

# ----------------------------------------------------
# core -> 이 아래 모든 코드들은 추후 모두 삭제 예정
from core.exceptions import CustomException
from core.error_codes import GlobalErrorCode
from core.base_response import BaseResponse
@app.get("/hello/{name}", response_model=BaseResponse)
async def say_hello(name: str):
    if name == "error":
        # 에러 테스트
        raise CustomException(GlobalErrorCode.INVALID_INPUT_VALUE)

    return BaseResponse.success_response(
        data={"greeting": f"Hello {name}"}
    )
