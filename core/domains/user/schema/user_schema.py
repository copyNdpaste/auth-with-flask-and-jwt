from pydantic.main import BaseModel


class UserResponseSchema(BaseModel):
    id: int
    nickname: str
