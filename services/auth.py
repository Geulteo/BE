from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from sqlalchemy.orm import Session

from config.settings import get_settings
from core.security import verify_password
from services import user as user_service
from models.user import User

settings = get_settings()

# 사용자 인증 및 토큰 관련 함수
def authenticate_user(db: Session, userid: str, password: str) -> User | None:
    # 사용자 ID로 DB에서 사용자 정보 가져옴
    db_user = user_service.get_user_by_userid(db, userid=userid)
    if not db_user:
        return None

    # 비밀번호 검증
    if not verify_password(password, db_user.password):
        return None

    return db_user

# JWT 토큰 생성 함수
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # 페이로드에 들어갈 데이터 복사
    to_encode = data.copy()

    # 만료 시간 설정
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 설정된 기본 만료 시간 사용
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # xp(만료 시간) 필드 추가
    to_encode.update({"exp": expire})

    # 토큰 인코딩(생성)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt