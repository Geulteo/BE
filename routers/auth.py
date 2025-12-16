from fastapi import APIRouter, Depends,status, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from models.user import UserCreateRequest, UserResponse, UserDeleteResponse
from models.auth import TokenRequest, TokenResponse
from database.session import get_db
from services import user as user_service
from services import auth as auth_service

from config.swagger_config import  get_current_user
from core.exceptions import CustomException
from core.error_codes import GlobalErrorCode
from core.base_response import BaseResponse
from services.auth import security

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]  # Swagger UI 태그
)

# 회원가입 (POST /auth/register)
@router.post(
    "/register",
    response_model=BaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    description="새로운 사용자를 등록합니다. userid가 이미 존재할 경우 400 에러를 반환합니다."
)
def register_user(
        user_data: UserCreateRequest,
        db: Session = Depends(get_db)
):

    # userid 중복 확인
    if user_service.get_user_by_userid(db, userid=user_data.userid):
        raise CustomException(GlobalErrorCode.INVALID_INPUT_VALUE, detail="이미 존재하는 사용자 ID입니다.")

    # 사용자 생성
    new_user = user_service.create_user(db=db, user_create=user_data)
    response_data = UserResponse.model_validate(new_user)

    # 응답 반환
    return BaseResponse.success_response(data=response_data, message="회원가입이 성공적으로 완료되었습니다.")

@router.delete(
    "/users/{id}",
    response_model=UserDeleteResponse,
    summary="사용자 탈퇴",
    description="로그인된 사용자가 Path Parameter로 지정된 사용자를 삭제합니다. 본인만 삭제 가능합니다."
)
def delete_user(
        id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
)-> UserDeleteResponse:
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
    return UserDeleteResponse(
        message="사용자가 성공적으로 삭제되었습니다.",
        detail=f"탈퇴된 사용자 ID: {db_user.userid}"
    )

@router.post("/login",
             response_model=BaseResponse,
             summary="로그인",
             description="userid와 password를 사용하여 JWT 토큰을 발급받습니다."
             )
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

    token_data = {"access_token": access_token, "token_type": "bearer"}

    return BaseResponse.success_response(data=token_data)

@router.post(
    "/logout",
    response_model=BaseResponse,
    summary="로그아웃",
    description="액세스 토큰을 서버의 블랙리스트에 등록하여 즉시 무효화합니다. (토큰 블랙리스트 처리)"
)
def logout_user(
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> BaseResponse:
    # credentials 객체에서 'Bearer '가 제거된 순수한 토큰 값만 추출
    token = credentials.credentials

    # 토큰을 블랙리스트에 추가
    auth_service.blacklist_token(db, token=token)

    # 응답 반환
    return BaseResponse.success_response(
        message="로그아웃이 성공적으로 처리되었으며 토큰이 무효화되었습니다."
    )