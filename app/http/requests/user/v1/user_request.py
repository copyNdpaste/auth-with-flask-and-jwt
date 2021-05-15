from pydantic import ValidationError
from pydantic import BaseModel

from app.extensions.utils.log_helper import logger_

from core.domains.user.dto.user_dto import SignupDto, SigninDto, UpdateUserDto

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


class SigninSchema(BaseModel):
    nickname: str = None
    password: str = None


class SigninRequest:
    def __init__(self, nickname, password):
        self.nickname = nickname
        self.password = password

    def validate_request_and_make_dto(self):
        try:
            SigninSchema(nickname=self.nickname, password=self.password)
            return self.to_dto()
        except ValidationError as e:
            logger.error(f"[SigninRequest][validate_request_and_make_dto] error : {e}")
            return False

    def to_dto(self) -> SigninDto:
        return SigninDto(nickname=self.nickname, password=self.password)


class UpdateUserSchema(BaseModel):
    user_id: int = None
    nickname: str = None
    new_nickname: str = None
    current_password: str = None
    current_password_check: str = None
    new_password: str = None


class UpdateUserRequest:
    def __init__(
        self,
        user_id: int = None,
        nickname: str = None,
        new_nickname: str = None,
        current_password: str = None,
        new_password: str = None,
        new_password_check: str = None,
    ):
        self.user_id = int(user_id) if user_id else None
        self.nickname = nickname or None
        self.new_nickname = new_nickname or None
        self.current_password = current_password or None
        self.new_password = new_password or None
        self.new_password_check = new_password_check or None

    def validate_request_and_make_dto(self):
        try:
            UpdateUserSchema(
                user_id=self.user_id,
                nickname=self.nickname,
                new_nickname=self.new_nickname,
                current_password=self.current_password,
                new_password=self.new_password,
                new_password_check=self.new_password_check,
            )
            return self.to_dto()
        except ValidationError as e:
            logger.error(
                f"[UpdateUserRequest][validate_request_and_make_dto] error : {e}"
            )
            return False

    def to_dto(self) -> UpdateUserDto:
        return UpdateUserDto(
            user_id=self.user_id,
            nickname=self.nickname,
            new_nickname=self.new_nickname,
            current_password=self.current_password,
            new_password=self.new_password,
            new_password_check=self.new_password_check,
        )
