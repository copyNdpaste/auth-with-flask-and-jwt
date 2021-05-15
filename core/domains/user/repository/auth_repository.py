from datetime import datetime
from typing import Optional

from app.extensions.database import session
from app.extensions.utils.log_helper import logger_
from app.persistence.model.auth_model import AuthModel

from core.domains.auth.entity.auth_entity import AuthEntity

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
            session.rollback()
            return False

    def update_auth(self, id: int) -> bool:
        try:
            session.query(AuthModel).filter_by(id=id).update({"is_verified": True})

            session.commit()

            return True
        except Exception as e:
            logger.error(f"[AuthRepository][update_auth] error : {e}")
            session.rollback()
            return False

    def get_auth(self, user_id: int, identification: str) -> Optional[AuthEntity]:
        auth = (
            session.query(AuthModel)
            .filter_by(user_id=user_id, identification=identification)
            .order_by(AuthModel.id.desc())
            .first()
        )

        return auth.to_entity() if auth else None
