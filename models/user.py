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
    userid: str
    password: str
    username: str

# 2. 응답 (Response) 모델

# 사용자 정보 응답
class UserResponse(BaseModel):
    id: int = Field(..., description="데이터베이스 ID")
    userid: str
    username: str

    class Config:
        # SQLAlchemy ORM 모델에서 Pydantic 모델로 변환 허용
        from_attributes = True

# 회원 탈퇴 응답
class UserDeleteResponse(BaseModel):
    message: str = "사용자가 성공적으로 삭제되었습니다."
    detail: str