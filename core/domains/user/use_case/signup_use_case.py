import inject

from core.domains.user.dto import UseCaseSuccessOutput
from core.domains.user.dto.user_dto import SignupDto
from core.domains.user.repository.user_repository import UserRepository


class SignupUseCase:
    @inject.autoparams()
    def __init__(self, user_repo: UserRepository):
        self.__user_repo = user_repo

    def execute(self, dto: SignupDto):
        user = self.__user_repo.signup(nickname=dto.nickname, password=dto.password)

        return UseCaseSuccessOutput(value=user)
