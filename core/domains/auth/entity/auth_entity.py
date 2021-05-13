from datetime import datetime
from pydantic import BaseModel

from core.domains.user.entity.user_entity import UserEntity


class AuthEntity(BaseModel):
    id: int = None
    user_id: int = None
    identification: str = None
    type: str = None
    verify_code: str = None
    is_verified: bool = None
    expired_at: datetime = None
    created_at: datetime = None
    updated_at: datetime = None
    user: UserEntity = None
