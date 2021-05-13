from datetime import datetime
from pydantic import BaseModel


class CreateAuthDto(BaseModel):
    user_id: int = None
    identification: str = None
    type_: str = None
    verify_code: str = None
    expired_at: datetime = None
