from typing import Optional
from urllib.parse import urlparse, urlunparse, quote
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    DB_URL: Optional[str] = None
    DB_USERNAME: Optional[str] = None
    DB_PASSWORD: Optional[str] = None

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
