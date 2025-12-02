from pydantic import BaseModel, Field


# 1. 요청 (Request) 모델

# 로그인 요청 스키마
class TokenRequest(BaseModel):
    userid: str = Field(
        ...,
        description="로그인할 사용자의 **고유 ID**입니다."
    )
    password: str = Field(
        ...,
        description="로그인할 사용자의 **비밀번호**입니다."
    )

# 2. 응답 (Response) 모델

# 서버 응답 (JWT 토큰) 스키마
class TokenResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="인증에 사용되는 **JWT 액세스 토큰**입니다."
    )
    token_type: str = Field(
        "bearer",
        description="토큰의 타입입니다. 일반적으로 'bearer'를 사용합니다."
    )