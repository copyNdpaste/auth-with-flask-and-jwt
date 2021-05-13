from core.domains.user.dto.user_dto import SignupDto
from core.domains.user.use_case.signup_use_case import SignupUseCase


def test_when_signup_then_success(session):
    dto = SignupDto(nickname="test_nickname", password="test_password")

    assert SignupUseCase().execute(dto=dto).value
