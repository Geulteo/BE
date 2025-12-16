from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from config.settings import get_settings
from core.security import verify_password
from services import user as user_service
from services import auth as auth_service
from models.user import User, BlacklistedToken

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
    token = credentials.credentials

    # 토큰 블랙리스트 검사
    if auth_service.is_token_blacklisted(db, token):
        raise CustomException(
            GlobalErrorCode.UNAUTHORIZED,
            detail="이 토큰은 이미 로그아웃 처리되었거나 무효화되었습니다.",
        )

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
    return {"sub": db_user.userid}


# 주어진 JWT 토큰을 블랙리스트에 추가, 이미 존재하면 오류를 무시
def blacklist_token(db: Session, token: str):
    try:
        # 토큰을 디코딩하여 만료 시각(exp)을 가져옴
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        expires_at_timestamp = payload.get("exp")
        if expires_at_timestamp:
            expires_at = datetime.fromtimestamp(expires_at_timestamp)
        else:
            return

        # BlacklistedToken 테이블에 저장
        db_token = BlacklistedToken(
            token=token,
            expires_at=expires_at
        )
        db.add(db_token)
        db.commit()

    # 유효하지 않은 토큰인 경우
    except JWTError:
        db.rollback()
        pass

    # 토큰이 이미 DB에 존재할 경우
    except IntegrityError:
        db.rollback()
        pass


# 주어진 토큰이 블랙리스트에 있는지 확인
def is_token_blacklisted(db: Session, token: str) -> bool:

    # 토큰이 테이블에 존재하는지 확인
    db_token = db.query(BlacklistedToken).filter(BlacklistedToken.token == token).first()

    # 블랙리스트에 있다면 True 반환
    if db_token:
        return True

    return False