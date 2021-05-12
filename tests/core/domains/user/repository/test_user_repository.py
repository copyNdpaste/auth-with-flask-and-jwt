from core.domains.user.repository.user_repository import UserRepository


def test_when_user_signup_then_success(session):
    nickname = "test_nickname"
    password = "test_password"

    assert UserRepository().signup(nickname=nickname, password=password)
