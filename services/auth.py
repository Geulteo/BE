from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from config.settings import get_settings
from core.security import verify_password
from services import user as user_service
from models.user import User

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.exceptions import CustomException
from core.error_codes import GlobalErrorCode
from database.session import get_db

settings = get_settings()

security = HTTPBearer()

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

# 현재 로그인 된 사용자 정보를 가져오는 의존성
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> dict:
    """
    Authorization: Bearer <token> 에서 토큰을 꺼내
    - JWT 디코딩
    - 사용자 존재 여부 확인
    후, {"sub": userid} 형태로 반환.
    (기존 delete_user에서 current_user.get("sub")로 쓰고 있으므로 dict로 맞춰줌)
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        raise CustomException(
            GlobalErrorCode.UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
        )

    userid: str | None = payload.get("sub")
    if userid is None:
        raise CustomException(
            GlobalErrorCode.UNAUTHORIZED,
            detail="토큰에 사용자 정보가 없습니다.",
        )

    db_user = user_service.get_user_by_userid(db, userid=userid)
    if db_user is None:
        raise CustomException(
            GlobalErrorCode.UNAUTHORIZED,
            detail="해당 사용자를 찾을 수 없습니다.",
        )

    # 기존 delete_user에서 current_user.get("sub")로 쓰고 있어서 그대로 맞춰줌
    return db_user