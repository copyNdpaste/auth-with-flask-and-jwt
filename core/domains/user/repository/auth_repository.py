from datetime import datetime

from app.extensions.database import session
from app.extensions.utils.log_helper import logger_
from app.persistence.model.auth_model import AuthModel

logger = logger_.getLogger(__name__)


class AuthRepository:
    def create_auth(
        self,
        user_id: int,
        identification: str,
        type_: str,
        verify_code: str,
        expired_at: datetime,
        is_verified: bool = False,
    ) -> bool:
        try:
            auth = AuthModel(
                user_id=user_id,
                identification=identification,
                type=type_,
                verify_code=verify_code,
                expired_at=expired_at,
                is_verified=is_verified,
            )

            session.add(auth)
            session.commit()

            return True
        except Exception as e:
            logger.error(f"[AuthRepository][create_auth] error : {e}")
            return False
