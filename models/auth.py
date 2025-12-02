from pydantic import BaseModel

# 1. 요청 (Request) 모델

# 로그인 요청 스키마
class TokenRequest(BaseModel):
    userid: str
    password: str

# 2. 응답 (Response) 모델

# 서버 응답 (JWT 토큰) 스키마
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"