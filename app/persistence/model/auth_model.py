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

    auth = relationship("UserModel", backref=backref("auth"))
