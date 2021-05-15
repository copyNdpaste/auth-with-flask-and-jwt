from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    DateTime,
)
from app import db
from app.extensions.utils.time_helper import get_utc_timestamp

from core.domains.user.entity.user_entity import UserEntity


class UserModel(db.Model):
    __tablename__ = "users"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    password = Column(String(100), nullable=False)
    nickname = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=get_utc_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=get_utc_timestamp(), nullable=False)

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            password=None,
            nickname=self.nickname,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
