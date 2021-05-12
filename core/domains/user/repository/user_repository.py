import bcrypt

from app.extensions.database import session
from app.extensions.utils.log_helper import logger_
from app.extensions.utils.time_helper import get_utc_timestamp
from app.persistence.model.user_model import UserModel

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
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
