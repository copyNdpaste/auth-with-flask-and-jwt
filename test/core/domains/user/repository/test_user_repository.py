import bcrypt

from core.domains.user.repository.user_repository import UserRepository


def test_when_user_signup_then_success(session):
    nickname = "test_nickname"
    password = "test_password"

    user = UserRepository().signup(nickname=nickname, password=password)

    assert user.nickname == nickname
    assert bcrypt.checkpw(password.encode("utf-8"), bytes(user.password))
