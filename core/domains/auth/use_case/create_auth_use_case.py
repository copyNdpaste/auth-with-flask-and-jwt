import inject
from datetime import datetime, timedelta
from random import randrange

from app.extensions.utils.log_helper import logger_
from app.extensions.utils.time_helper import get_utc_timestamp

from core.domains.auth.dto.auth_dto import CreateAuthDto
from core.domains.auth.enum.auth_enum import VerifyWayEnum
from core.domains.user.repository.auth_repository import AuthRepository
from core.domains.user.repository.user_repository import UserRepository
from core.use_case_output import FailureType, UseCaseFailureOutput, UseCaseSuccessOutput


logger = logger_.getLogger(__name__)


class CreateAuthUseCase:
    @inject.autoparams()
    def __init__(self, auth_repo: AuthRepository, user_repo: UserRepository):
        self.__auth_repo = auth_repo
        self.__user_repo = user_repo

    def execute(self, dto: CreateAuthDto):
        user = self.__user_repo.get_user(user_id=dto.user_id)
        if not user:
            return UseCaseFailureOutput(type=FailureType.NOT_FOUND_ERROR)

        dto.expired_at = self.__create_expired_at()
        dto.verify_code = self.__create_verify_code()

        result = self.__auth_repo.create_auth(
            user_id=dto.user_id,
            identification=dto.identification,
            type_=dto.type_,
            verify_code=dto.verify_code,
            expired_at=dto.expired_at,
        )
        if not result:
            return UseCaseFailureOutput(type=FailureType.INSERT_ERROR)

        self.__send_verify_code(type_=dto.type_, verify_code=dto.verify_code)

        return UseCaseSuccessOutput(value=result)

    def __create_expired_at(self) -> datetime:
        return get_utc_timestamp() + timedelta(minutes=3)

    def __create_verify_code(self) -> str:
        return str(randrange(100000, 999999))

    def __send_verify_code(self, type_: str, verify_code: str) -> None:
        if type_ == VerifyWayEnum.EMAIL.value:
            ...
        elif type_ == VerifyWayEnum.SMS.value:
            ...
        logger.info(
            f"[CreateAuthUseCase][__send_verify_code] send verify_code by {type_}"
        )
        logger.info(
            f"[CreateAuthUseCase][__send_verify_code] verify_code : {verify_code}"
        )
