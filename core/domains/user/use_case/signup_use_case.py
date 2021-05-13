import inject

from core.domains.user.dto.user_dto import SignupDto
from core.domains.user.repository.user_repository import UserRepository
from core.use_case_output import FailureType, UseCaseFailureOutput, UseCaseSuccessOutput


class SignupUseCase:
    @inject.autoparams()
    def __init__(self, user_repo: UserRepository):
        self.__user_repo = user_repo

    def execute(self, dto: SignupDto):
        result = self.__user_repo.signup(nickname=dto.nickname, password=dto.password)

        if not result:
            return UseCaseFailureOutput(type=FailureType.INSERT_ERROR)

        return UseCaseSuccessOutput(value=result)
