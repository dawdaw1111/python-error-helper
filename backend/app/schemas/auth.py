from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=120)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    expires_in: int


class AdminProfile(BaseModel):
    username: str
