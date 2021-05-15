from core.domains.user.dto.user_dto import SigninDto
from core.domains.user.repository.user_repository import UserRepository
from core.domains.user.use_case.signin_use_case import SigninUseCase
from core.use_case_output import FailureType, UseCaseFailureOutput


def test_when_signin_then_success(session):
    nickname = "test_nickname"
    password = "test_password"

    UserRepository().signup(nickname=nickname, password=password)

    dto = SigninDto(nickname="test_nickname", password="test_password")

    assert isinstance(SigninUseCase().execute(dto=dto).value, str)


def test_when_signin_with_incorrect_password_then_unauthorized_error(session):
    nickname = "test_nickname"
    password = "test_password"

    UserRepository().signup(nickname=nickname, password=password)

    dto = SigninDto(nickname="test_nickname", password="test_passwor")

    result = SigninUseCase().execute(dto=dto)

    assert isinstance(result, UseCaseFailureOutput)
    assert result.value["type"] == FailureType.UNAUTHORIZED_ERROR
