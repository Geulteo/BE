from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from models.user import UserCreate, UserResponse, Token, TokenRequest
from database.session import get_db
from services import user as user_service
from services import auth as auth_service

from config.swagger_config import  get_current_user
from core.exceptions import CustomException
from core.error_codes import GlobalErrorCode

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]  # Swagger UI 태그
)

# 회원가입 (POST /auth/register)
@router.post(
    "/register",
    response_model=UserResponse,  # 응답 데이터 형식 지정
    status_code=status.HTTP_201_CREATED,  # 성공 시 HTTP 201 Created 반환
)
def register_user(
        user_data: UserCreate,  # 요청 바디를 models.UserCreate 스키마로 받음
        db: Session = Depends(get_db)  # database.session.get_db 함수를 통해 DB 세션 주입
):

    # userid 중복 확인
    if user_service.get_user_by_userid(db, userid=user_data.userid):
        raise CustomException(GlobalErrorCode.INVALID_INPUT_VALUE, detail="이미 존재하는 사용자 ID입니다.")

    # 사용자 생성
    new_user = user_service.create_user(db=db, user_create=user_data)

    # 응답 반환
    return new_user

# (DELETE /auth/users/{id})
@router.delete(
    "/users/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
        id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    # 사용자 존재 확인
    db_user = user_service.get_user_by_id(db, id_=id)
    if db_user is None:
        raise CustomException(GlobalErrorCode.RESOURCE_NOT_FOUND, detail=f"사용자 ID {id}를 찾을 수 없습니다.")

    # 사용자 본인 확인
    logged_in_userid = current_user.get("sub")

    if logged_in_userid != db_user.userid:
        raise CustomException(GlobalErrorCode.FORBIDDEN)

    # 사용자 삭제
    user_service.delete_user(db, db_user=db_user)
    return

# 로그인 (POST /auth/login)
@router.post("/login", response_model=Token)
def login_for_access_token(
        form_data: TokenRequest,
        db: Session = Depends(get_db)
):
    user = user_service.get_user_by_userid(db, userid=form_data.userid)

    # 사용자 존재 및 비밀번호 검증
    if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
        raise CustomException(GlobalErrorCode.UNAUTHORIZED, detail="사용자 ID가 존재하지 않거나 비밀번호가 일치하지 않습니다.")

    # JWT 토큰 생성
    access_token = auth_service.create_access_token(
        data={"sub": user.userid}
    )

    # 토큰 반환
    return {"access_token": access_token, "token_type": "bearer"}