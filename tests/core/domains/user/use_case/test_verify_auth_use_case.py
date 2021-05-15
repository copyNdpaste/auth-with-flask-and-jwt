from datetime import timedelta

from app.extensions.utils.time_helper import get_utc_timestamp

from core.domains.auth.dto.auth_dto import VerifyAuthDto
from core.domains.auth.use_case.verify_auth_use_case import VerifyAuthUseCase
from core.domains.user.repository.auth_repository import AuthRepository
from core.domains.user.repository.user_repository import UserRepository


def test_when_verify_auth_then_success(session):
    UserRepository().signup(nickname="test_nickname", password="test_password")
    AuthRepository().create_auth(
        user_id=1,
        identification="test@email.com",
        type_="email",
        verify_code="1234",
        expired_at=get_utc_timestamp() + timedelta(minutes=3),
    )

    dto = VerifyAuthDto(user_id=1, identification="test@email.com", verify_code="1234")

    assert VerifyAuthUseCase().execute(dto=dto).value

    auth = AuthRepository().get_auth(user_id=1, identification="test@email.com")
    assert auth.is_verified
