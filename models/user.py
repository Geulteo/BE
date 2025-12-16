from sqlalchemy import Column, Integer, String, DateTime
from pydantic import BaseModel, Field
from database.session import Base

# 사용자 모델 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True,index=True)
    userid = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    username = Column(String(50), index=True)

# 로그아웃된 토큰(Blacklist) 모델 정의
class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), unique=True, index=True)
    expires_at = Column(DateTime)

# 회원 가입 요청 데이터
class UserCreateRequest(BaseModel):
    userid: str
    password: str
    username: str

# 사용자 정보 응답
class UserResponse(BaseModel):
    id: int
    userid: str
    username: str

    class Config:
        from_attributes = True

# 회원 탈퇴 응답
class UserDeleteResponse(BaseModel):
    message: str
    detail: str