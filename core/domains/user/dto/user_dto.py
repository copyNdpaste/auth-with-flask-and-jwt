from pydantic import BaseModel


class SignupDto(BaseModel):
    nickname: str = None
    password: str = None


class SigninDto(BaseModel):
    nickname: str = None
    password: str = None


class UpdateUserDto(BaseModel):
    user_id: int = None
    nickname: str = None
    new_nickname: str = None
    current_password: str = None
    current_password_check: str = None
    new_password: str = None
