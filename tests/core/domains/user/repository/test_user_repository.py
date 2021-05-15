from core.domains.user.entity.user_entity import UserEntity
from core.domains.user.repository.user_repository import UserRepository


def test_user_signup_then_success(session):
    nickname = "test_nickname"
    password = "test_password"

    assert UserRepository().signup(nickname=nickname, password=password)


def test_user_signin_then_success(session):
    nickname = "test_nickname"
    password = "test_password"

    UserRepository().signup(nickname=nickname, password=password)

    user = UserRepository().signin(nickname=nickname, password=password)

    assert isinstance(user, UserEntity)
    assert user.id == 1


def test_user_signin_with_incorrect_password_then_fail(session):
    nickname = "test_nickname"
    password = "test_password"

    UserRepository().signup(nickname=nickname, password=password)

    result = UserRepository().signin(nickname=nickname, password="test_passwor")

    assert result == False


def test_user_signin_with_incorrect_nickname_then_fail(session):
    nickname = "test_nickname"
    password = "test_password"

    UserRepository().signup(nickname=nickname, password=password)

    result = UserRepository().signin(nickname="nick", password=password)

    assert result == False


def test_user_update_user_info_then_success(session):
    nickname = "test_nickname"
    password = "test_password"

    UserRepository().signup(nickname=nickname, password=password)

    assert UserRepository().update_user(user_id=1, nickname="nick", password=password)


def test_not_exist_user_update_user_info_then_fail(session):
    assert (
        UserRepository().update_user(user_id=0, nickname="nick", password="1234") == 0
    )
