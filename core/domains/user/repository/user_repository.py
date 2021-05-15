import bcrypt
from typing import Union

from app.extensions.database import session
from app.extensions.utils.log_helper import logger_
from app.extensions.utils.time_helper import get_utc_timestamp
from app.persistence.model.user_model import UserModel

from core.domains.user.entity.user_entity import UserEntity

logger = logger_.getLogger(__name__)


class UserRepository:
    def signup(self, nickname: str, password: str) -> bool:
        try:
            encrypted_password = self.__encrypt_password(password=password)
            user = UserModel(
                nickname=nickname,
                password=encrypted_password,
                created_at=get_utc_timestamp(),
                updated_at=get_utc_timestamp(),
            )

            session.add(user)
            session.commit()

            return True
        except Exception as e:
            logger.error(f"[UserRepository][signup] error : {e}")
            return False

    def __encrypt_password(self, password: str) -> bytes:
        encoded_password = self.__encode_password(password=password)
        return bcrypt.hashpw(encoded_password, bcrypt.gensalt())

    def __encode_password(self, password: str, type_: str = "utf-8") -> bytes:
        return password.encode(type_)

    def get_user(self, user_id: int) -> Union[UserEntity, bool]:
        try:
            user = session.query(UserModel).filter_by(id=user_id).first()

            return user.to_entity() if user else None
        except Exception as e:
            logger.error(f"[UserRepository][get_user] error : {e}")
            return False

    def signin(self, nickname: str, password: str) -> Union[UserEntity, bool]:
        try:
            user = session.query(UserModel).filter_by(nickname=nickname).first()

            if user:
                encoded_password = self.__encode_password(password=password)
                encrypted_password = user.password
                if bcrypt.checkpw(encoded_password, encrypted_password):
                    return user.to_entity()
            return False
        except Exception as e:
            logger.error(f"[UserRepository][signin] error : {e}")
            return False

    def update_user(
        self, user_id: int, nickname: str = None, password: str = None
    ) -> bool:
        dct = {}
        if nickname:
            dct["nickname"] = nickname
        if password:
            dct["password"] = password
        try:
            return session.query(UserModel).filter_by(id=user_id).update(dct)
        except Exception as e:
            logger.error(f"[UserRepository][update_user] error : {e}")
            session.rollback()
            return False
