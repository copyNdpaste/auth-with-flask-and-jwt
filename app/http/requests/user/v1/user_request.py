from pydantic import ValidationError
from pydantic.main import BaseModel

from app.extensions.utils.log_helper import logger_

from core.domains.user.dto.user_dto import SignupDto

logger = logger_.getLogger(__name__)


class SignupSchema(BaseModel):
    nickname: str = None
    password: str = None


class SignupRequest:
    def __init__(self, nickname, password):
        self.nickname = nickname
        self.password = password

    def validate_request_and_make_dto(self):
        try:
            SignupSchema(nickname=self.nickname, password=self.password)
            return self.to_dto()
        except ValidationError as e:
            logger.error(f"[SignupRequest][validate_request_and_make_dto] error : {e}")
            return False

    def to_dto(self) -> SignupDto:
        return SignupDto(nickname=self.nickname, password=self.password)
