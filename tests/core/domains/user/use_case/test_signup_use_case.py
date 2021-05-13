from core.domains.user.dto.user_dto import SignupDto
from core.domains.user.use_case.signup_use_case import SignupUseCase


def test_when_signup_then_success(session):
    nickname = "test_nickname"
    password = "test_password"

    dto = SignupDto(nickname=nickname, password=password)

    assert SignupUseCase().execute(dto=dto).value
