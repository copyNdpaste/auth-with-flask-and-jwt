from datetime import timedelta

from app.extensions.utils.time_helper import get_utc_timestamp

from core.domains.auth.entity.auth_entity import AuthEntity
from core.domains.user.repository.auth_repository import AuthRepository
from core.domains.user.repository.user_repository import UserRepository


def test_create_auth_repo_then_success(session):
    UserRepository().signup(nickname="test_nickname", password="test_password")

    result = AuthRepository().create_auth(
        user_id=1,
        identification="test@email.com",
        type_="email",
        verify_code="1234",
        expired_at=get_utc_timestamp() + timedelta(minutes=3),
    )

    assert result


def test_update_auth_then_success(session):
    UserRepository().signup(nickname="test_nickname", password="test_password")
    AuthRepository().create_auth(
        user_id=1,
        identification="test@email.com",
        type_="email",
        verify_code="1234",
        expired_at=get_utc_timestamp() + timedelta(minutes=3),
    )

    assert AuthRepository().update_auth(id=1)


def test_get_auth_then_success(session):
    UserRepository().signup(nickname="test_nickname", password="test_password")
    AuthRepository().create_auth(
        user_id=1,
        identification="test@email.com",
        type_="email",
        verify_code="1234",
        expired_at=get_utc_timestamp() + timedelta(minutes=3),
    )

    auth = AuthRepository().get_auth(user_id=1, identification="test@email.com")

    assert isinstance(auth, AuthEntity)
