from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship, backref
from app import db
from app.extensions.utils.time_helper import get_utc_timestamp_for_model


class UserModel(db.Model):
    __tablename__ = "users"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    password = Column(String(100), nullable=False)
    nickname = Column(String(50), nullable=False)
    created_at = Column(
        DateTime, server_default=get_utc_timestamp_for_model(), nullable=False
    )
    updated_at = Column(
        DateTime, server_default=get_utc_timestamp_for_model(), nullable=False
    )

    auth = relationship("AuthModel", backref=backref("user"))

    # def to_entity(self) -> UserEntity:
    #     return UserEntity(
    #         id=self.id,
    #         password=self.password,
    #         nickname=self.nickname,
    #         created_at=self.created_at,
    #         updated_at=self.updated_at,
    #         auth=self.auth,
    #     )
