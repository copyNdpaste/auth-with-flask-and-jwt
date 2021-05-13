import inject

from app.extensions.utils.log_helper import logger_
from app.extensions.utils.time_helper import get_utc_timestamp

from core.domains.auth.dto.auth_dto import VerifyAuthDto
from core.domains.auth.entity.auth_entity import AuthEntity
from core.domains.user.repository.auth_repository import AuthRepository
from core.domains.user.repository.user_repository import UserRepository
from core.use_case_output import FailureType, UseCaseFailureOutput, UseCaseSuccessOutput


logger = logger_.getLogger(__name__)


class VerifyAuthUseCase:
    @inject.autoparams()
    def __init__(self, auth_repo: AuthRepository, user_repo: UserRepository):
        self.__auth_repo = auth_repo
        self.__user_repo = user_repo

    def execute(self, dto: VerifyAuthDto):
        user = self.__user_repo.get_user(user_id=dto.user_id)
        if not user:
            return UseCaseFailureOutput(type=FailureType.NOT_FOUND_ERROR)

        auth = self.__auth_repo.get_auth(
            user_id=dto.user_id, identification=dto.identification
        )

        is_verified = self.__verify_auth(auth=auth, verify_code=dto.verify_code)
        if not is_verified:
            return UseCaseFailureOutput(type=FailureType.UNAUTHORIZED_ERROR)

        self.__auth_repo.update_auth(id=auth.id)

        return UseCaseSuccessOutput(value=is_verified)

    def __verify_auth(self, auth: AuthEntity, verify_code: str) -> bool:
        current_datetime = get_utc_timestamp()
        if auth.verify_code == verify_code and current_datetime <= auth.expired_at:
            return True
        return False
