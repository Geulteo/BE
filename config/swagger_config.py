from fastapi import FastAPI, HTTPException, status, Request
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
import os

from jose import jwt, JWTError
from config.settings import get_settings

# JWT Bearer 토큰 스키마
security = HTTPBearer(auto_error=False)

settings = get_settings()

# JWT 디코딩 함수
def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


# 토큰 인증 의존성
async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = None
    
    # 1. 먼저 쿠키에서 토큰 확인
    token = request.cookies.get("accessToken")
    
    # 2. 쿠키에 없으면 Authorization 헤더에서 확인
    if not token and credentials:
        token = credentials.credentials
    
    # 3. 토큰이 없으면 401 에러
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    
    payload = decode_jwt_token(token)
    return payload

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    # 서버 정보 설정
    context_path = os.getenv("CONTEXT_PATH", "")

    openapi_schema = get_openapi(
        title="자연어처리 API 명세서",
        version="1.0",
        description="NLP Swagger API Documentation",
        routes=app.routes,
        servers=[
            {
                "url": context_path,
                "description": "NLP Server"
            }
        ]
    )

    components = openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})

    # JWT Bearer 인증 스키마 추가
    security_schemes["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


def setup_swagger(app: FastAPI):
    app.openapi = lambda: custom_openapi(app)

    # Swagger UI 및 ReDoc 설정
    app.docs_url = "/swagger-ui"
    app.redoc_url = "/redoc"
    app.openapi_url = "/openapi.json"


# main.py에서 사용할 설정 함수
def create_app() -> FastAPI:
    app = FastAPI(
        title="NLP API",
        description="NLP Swagger API Documentation",
        version="1.0",
        docs_url=None,
        redoc_url=None
    )

    # Swagger 설정 적용
    setup_swagger(app)

    return app