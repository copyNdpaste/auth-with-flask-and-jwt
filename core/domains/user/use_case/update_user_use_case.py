import inject

from core.domains.user.dto.user_dto import UpdateUserDto
from core.domains.user.repository.user_repository import UserRepository
from core.use_case_output import FailureType, UseCaseFailureOutput, UseCaseSuccessOutput


class UpdateUserUseCase:
    @inject.autoparams()
    def __init__(self, user_repo: UserRepository):
        self.__user_repo = user_repo

    def execute(self, dto: UpdateUserDto):
        if (
            not dto.nickname
            and not dto.new_nickname
            and not dto.current_password
            and not dto.new_password
            and not dto.new_password_check
        ):
            return UseCaseFailureOutput(
                type=FailureType.INVALID_REQUEST_ERROR, message="no input parameter"
            )

        user = self.__user_repo.get_user(user_id=dto.user_id)
        if not user:
            return UseCaseFailureOutput(
                type=FailureType.NOT_FOUND_ERROR, message="user not found"
            )

        dto.nickname = user.nickname

        if dto.nickname == dto.new_nickname:
            return UseCaseFailureOutput(
                type=FailureType.INVALID_REQUEST_ERROR, message="nickname unchanged"
            )

        if dto.new_password != dto.new_password_check:
            return UseCaseFailureOutput(
                type=FailureType.INVALID_REQUEST_ERROR,
                message="new password checking failed",
            )

        if dto.new_password and not self.__user_repo.check_password(
            user_id=dto.user_id, input_password=dto.current_password
        ):
            return UseCaseFailureOutput(
                type=FailureType.INVALID_REQUEST_ERROR,
                message="current password checking failed",
            )

        if dto.new_password and dto.new_password == dto.current_password:
            return UseCaseFailureOutput(
                type=FailureType.INVALID_REQUEST_ERROR, message="password unchanged"
            )

        if dto.current_password and not dto.new_password:
            return UseCaseFailureOutput(
                type=FailureType.INVALID_REQUEST_ERROR,
                message="new password not delivered",
            )

        user = self.__user_repo.update_user(
            user_id=dto.user_id, nickname=dto.nickname, password=dto.new_password
        )

        if not user:
            return UseCaseFailureOutput(type=FailureType.UPDATE_ERROR)

        return UseCaseSuccessOutput(value=True)
