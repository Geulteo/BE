from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import UserCreate, UserResponse
from database.session import get_db
from services import user as user_service

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

    # userid 중복 확인 (이메일 중복 확인 로직 대체)
    if user_service.get_user_by_userid(db, userid=user_data.userid):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 존재하는 사용자 ID입니다."
        )

    # 사용자 이름 중복 확인
    if user_service.get_user_by_username(db, username=user_data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 존재하는 사용자 이름입니다."
        )

    # 사용자 생성
    new_user = user_service.create_user(db=db, user_create=user_data)

    # 응답 반환
    return new_user

# 전체 사용자 조회 (GET /auth/users)
@router.get(
    "/users",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_users(
        db: Session = Depends(get_db),
        skip: int = 0, # 건너뛸 항목 수
        limit: int = 100 # 최대 항목 수
):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

# (DELETE /auth/users/{id})
@router.delete(
    "/users/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
        id: int,
        db: Session = Depends(get_db)
):
    # 사용자 존재 확인
    db_user = user_service.get_user_by_id(db, id_=id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"사용자 ID {id}를 찾을 수 없습니다."
        )

    # 사용자 삭제
    user_service.delete_user(db, db_user=db_user)
    return