from pydantic import BaseModel


class SignupDto(BaseModel):
    nickname: str = None
    password: str = None


class SigninDto(BaseModel):
    nickname: str = None
    password: str = None
