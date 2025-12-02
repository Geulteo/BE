from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, Field
from database.session import Base

# DB 테이블 구조 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True,index=True)
    userid = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    username = Column(String(50), index=True)

# 1. 요청 (Request) 모델

# 회원 가입 요청 데이터
class UserCreateRequest(BaseModel):
    userid: str = Field(
        ...,
        description="사용자가 로그인에 사용할 **고유 ID**입니다."
    )
    password: str = Field(
        ...,
        description="사용자의 **비밀번호**입니다. (안전을 위해 해시되어 저장됨)"
    )
    username: str = Field(
        ...,
        description="사용자의 **이름** 또는 닉네임입니다."
    )

# 2. 응답 (Response) 모델

# 사용자 정보 응답
class UserResponse(BaseModel):
    id: int = Field(
        ...,
        description="데이터베이스에서 관리되는 사용자 **고유 ID**입니다."
    )
    userid: str = Field(
        ...,
        description="로그인에 사용되는 **사용자 ID**입니다."
    )
    username: str = Field(
        ...,
        description="사용자의 **이름**입니다."
    )

    class Config:
        # SQLAlchemy ORM 모델에서 Pydantic 모델로 변환 허용
        from_attributes = True

# 회원 탈퇴 응답
class UserDeleteResponse(BaseModel):
    message: str = Field(
        "사용자가 성공적으로 삭제되었습니다.",
        description="API 실행 결과에 대한 응답 메시지입니다."
    )
    detail: str = Field(
        ...,
        description="삭제된 사용자 ID 등 상세 정보가 포함됩니다."
    )