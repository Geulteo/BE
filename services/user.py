from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from models.user import User, UserCreate
from typing import Optional

# 비밀번호 해싱을 위한 컨텍스트 객체
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 암호화
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# # 사용자 조회
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, id_: int) -> Optional[User]:
    return db.query(User).filter(User.id == id_).first()

def get_user_by_userid(db: Session, userid: str) -> Optional[User]:
    return db.query(User).filter(User.userid == userid).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

# 회원가입 서비스
def create_user(db: Session, user_create: UserCreate) -> User:

    # 비밀번호 암호화
    hashed_password = get_password_hash(user_create.password)

    # DB 모델 인스턴스 생성
    db_user = User(
        userid=user_create.userid,
        hashed_password=hashed_password,
        username=user_create.username,
    )

    # DB 세션에 추가 및 커밋
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        db.rollback()
        raise ValueError("이미 존재하는 사용자 이름 또는 이메일입니다.")

    return db_user

# 회원 탈퇴 서비스
def delete_user(db: Session, db_user):

    db.delete(db_user)
    db.commit()

    return