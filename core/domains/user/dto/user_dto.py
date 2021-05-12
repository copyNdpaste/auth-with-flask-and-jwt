from pydantic.main import BaseModel


class SignupDto(BaseModel):
    nickname: str = None
    password: str = None
