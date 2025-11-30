from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from database.session import Base

# DB 테이블 구조 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    username = Column(String(50), index=True)

# 클라이언트 요청 스키마 정의
class UserCreate(BaseModel):
    userid: str  # <- 새로운 userid 필드
    password: str
    username: str

# 서버 응답 스키마 정의
class UserResponse(BaseModel):
    id: int
    userid: str
    username: str

    # ORM 모델(User 클래스)의 인스턴스를 Pydantic 모델로 변환할 수 있도록 설정
    class Config:
        from_attributes = True