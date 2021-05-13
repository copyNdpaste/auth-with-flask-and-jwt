from sqlalchemy import (
    Column,
    DateTime,
    BigInteger,
    Integer,
    ForeignKey,
    String,
    Boolean,
)
from sqlalchemy.orm import relationship, backref

from app import db
from app.extensions.utils.time_helper import get_utc_timestamp
from app.persistence.model.user_model import UserModel

from core.domains.auth.entity.auth_entity import AuthEntity


class AuthModel(db.Model):
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    user_id = Column(BigInteger, ForeignKey(UserModel.id), nullable=False)
    identification = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)
    verify_code = Column(String(50), nullable=False)
    is_verified = Column(Boolean)
    expired_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=get_utc_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=get_utc_timestamp(), nullable=False)

    user = relationship("UserModel", backref=backref("auth"))

    def to_entity(self) -> AuthEntity:
        return AuthEntity(
            id=self.id,
            user_id=self.user_id,
            identification=self.identification,
            type=self.type,
            verify_code=self.verify_code,
            is_verified=self.is_verified,
            expired_at=self.expired_at,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user=self.user.to_entity() if self.user else None,
        )
