from datetime import timedelta

from app.extensions.utils.time_helper import get_utc_timestamp

from core.domains.auth.dto.auth_dto import CreateAuthDto
from core.domains.auth.use_case.create_auth_use_case import CreateAuthUseCase
from core.domains.user.repository.user_repository import UserRepository


def test_when_create_auth_then_success(session):
    UserRepository().signup(nickname="test_nickname", password="test_password")

    dto = CreateAuthDto(
        user_id=1,
        identification="test@email.com",
        type_="email",
        verify_code="1234",
        expired_at=get_utc_timestamp() + timedelta(minutes=3),
    )

    assert CreateAuthUseCase().execute(dto=dto).value
