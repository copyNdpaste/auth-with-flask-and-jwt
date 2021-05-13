from datetime import datetime
from pydantic import BaseModel


class UserEntity(BaseModel):
    id: int = None
    nickname: str = None
    created_at: datetime = None
    updated_at: datetime = None
