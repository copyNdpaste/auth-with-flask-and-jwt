from pydantic import BaseModel


class UserResponseSchema(BaseModel):
    id: int
    nickname: str
