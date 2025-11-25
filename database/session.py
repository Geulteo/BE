from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config.settings import get_settings

settings = get_settings()
SQLALCHEMY_DATABASE_URL = settings.database_url_sync()

# 동기 엔진
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

# 동기 세션팩토리
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base 클래스 (모든 모델이 상속)
Base = declarative_base()
