from typing import Optional
from urllib.parse import urlparse, urlunparse, quote
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Qdrant 설정 (배포 시 .env에서 주입)
    QDRANT_HOST: str = "qdrant"   # docker-compose 기준 서비스 이름
    QDRANT_PORT: int = 6333
    QDRANT_DIFFICULTY_COLLECTION: str = "difficulty_cards"
    QDRANT_USER_SENTENCE_COLLECTION: str = "user_sentences"

    # SBERT / Embedding 모델
    SBERT_MODEL_NAME: str = "jhgan/ko-sbert-multitask"
    SBERT_DIM: int = 768

    # Qdrant 접속 URL 유틸 (QdrantClient(url=...)에 바로 사용)
    def qdrant_url(self) -> str:
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    # LLM 설정
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    DB_URL: Optional[str] = None
    DB_USERNAME: Optional[str] = None
    DB_PASSWORD: Optional[str] = None

    # JWT 설정
    SECRET_KEY: str  # JWT 서명에 사용할 비밀 키
    ALGORITHM: str = "HS256"  # JWT 암호화 알고리즘
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 액세스 토큰 만료 시간 (분)

    CORS_ORIGINS: Optional[str] = "*"   # 기본은 전체 허용 (개발용)

    def database_url_sync(self) -> str:
        if not self.DB_URL:
            raise ValueError("환경변수 DB_URL이 필요합니다.")

        raw = self.DB_URL.strip()

        # jdbc: 접두사 제거
        if raw.startswith("jdbc:"):
            raw = raw[len("jdbc:"):]

        parsed = urlparse(raw)

        if parsed.scheme != "mysql":
            raise ValueError(f"지원하지 않는 DB 스킴입니다: {parsed.scheme}")

        username = self.DB_USERNAME or ""
        password = self.DB_PASSWORD or ""

        host_port = parsed.netloc.split("@")[-1]

        cred = ""
        if username or password:
            cred = quote(username)
            if password:
                cred += f":{quote(password)}"
            cred += "@"

        # 동기용 드라이버 스킴으로 교체
        new_scheme = "mysql+pymysql"
        new_netloc = cred + host_port

        new_parsed = parsed._replace(scheme=new_scheme, netloc=new_netloc)
        dsn = str(urlunparse(new_parsed))

        return dsn

# 캐싱
@lru_cache
def get_settings() -> Settings:
    return Settings()
