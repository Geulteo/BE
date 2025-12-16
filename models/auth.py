from pydantic import BaseModel, Field

# 로그인 요청 스키마
class TokenRequest(BaseModel):
    userid: str
    password: str

# 서버 응답 (JWT 토큰) 스키마
class TokenResponse(BaseModel):
    token_type: str
    access_token: str