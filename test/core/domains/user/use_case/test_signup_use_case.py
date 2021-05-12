import bcrypt

from core.domains.user.dto.user_dto import SignupDto
from core.domains.user.use_case.signup_use_case import SignupUseCase


def test_when_signup_then_success(session):
    nickname = "test_nickname"
    password = "test_password"

    dto = SignupDto(nickname=nickname, password=password)

    result = SignupUseCase().execute(dto=dto)
    user = result.value

    assert user.nickname == nickname
    assert bcrypt.checkpw(password.encode("utf-8"), bytes(user.password))
