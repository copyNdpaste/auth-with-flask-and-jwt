import inject
from flask_jwt_extended import create_access_token

from core.domains.user.dto.user_dto import SigninDto
from core.domains.user.repository.user_repository import UserRepository
from core.use_case_output import FailureType, UseCaseFailureOutput, UseCaseSuccessOutput


class SigninUseCase:
    @inject.autoparams()
    def __init__(self, user_repo: UserRepository):
        self.__user_repo = user_repo

    def execute(self, dto: SigninDto):
        user = self.__user_repo.signin(nickname=dto.nickname, password=dto.password)

        if not user:
            return UseCaseFailureOutput(type=FailureType.UNAUTHORIZED_ERROR)

        jwt = self.__create_jwt(user_id=user.id)

        return UseCaseSuccessOutput(value=jwt)

    def __create_jwt(self, user_id: int) -> str:
        return create_access_token(identity=user_id)
