from pydantic import ValidationError
from pydantic import BaseModel

from app.extensions.utils.log_helper import logger_

from core.domains.auth.dto.auth_dto import CreateAuthDto


logger = logger_.getLogger(__name__)


class CreateAuthSchema(BaseModel):
    user_id: int = None
    identification: str = None
    type_: str = None


class CreateAuthRequest:
    def __init__(self, user_id, identification, type_):
        self.user_id = user_id
        self.identification = identification
        self.type_ = type_

    def validate_request_and_make_dto(self):
        try:
            CreateAuthSchema(
                user_id=self.user_id,
                identification=self.identification,
                type_=self.type_,
            )
            return self.to_dto()
        except ValidationError as e:
            logger.error(
                f"[CreateAuthRequest][validate_request_and_make_dto] error : {e}"
            )
            return False

    def to_dto(self) -> CreateAuthDto:
        return CreateAuthDto(
            user_id=self.user_id,
            identification=self.identification,
            type_=self.type_,
        )
