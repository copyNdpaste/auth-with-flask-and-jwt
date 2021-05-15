import pytest

from core.domains.user.dto.user_dto import UpdateUserDto
from core.domains.user.repository.user_repository import UserRepository
from core.domains.user.use_case.update_user_use_case import UpdateUserUseCase
from core.use_case_output import FailureType, UseCaseSuccessOutput


@pytest.mark.parametrize(
    "new_nickname, current_password, new_password, new_password_check, result, msg",
    [
        # update : nickname, password
        ("new_nickname", "test_password", "new_password", "new_password", True, None),
        # update: password
        (None, "test_password", "new_password", "new_password", True, None),
        (
            "test_nickname",
            "test_password",
            "new_password",
            "new_password",
            FailureType.INVALID_REQUEST_ERROR,
            "nickname unchanged",
        ),
        (
            None,
            "test_password",
            "new_passwor",
            "new_password",
            FailureType.INVALID_REQUEST_ERROR,
            "new password checking failed",
        ),
        (
            None,
            "test_passwor",
            "new_password",
            "new_password",
            FailureType.INVALID_REQUEST_ERROR,
            "current password checking failed",
        ),
        (
            None,
            "test_password",
            "test_password",
            "test_password",
            FailureType.INVALID_REQUEST_ERROR,
            "password unchanged",
        ),
        (
            None,
            None,
            None,
            None,
            FailureType.INVALID_REQUEST_ERROR,
            "no input parameter",
        ),
    ],
)
def test_when_update_user(
    session,
    new_nickname,
    current_password,
    new_password,
    new_password_check,
    result,
    msg,
):
    UserRepository().signup(nickname="test_nickname", password="test_password")

    dto = UpdateUserDto(
        user_id=1,
        new_nickname=new_nickname,
        current_password=current_password,
        new_password=new_password,
        new_password_check=new_password_check,
    )

    output = UpdateUserUseCase().execute(dto=dto)
    if isinstance(output, UseCaseSuccessOutput):
        assert output.value == result
        user = UserRepository().get_user(user_id=1)
        assert user.nickname is not None
    else:
        assert output.type == result

    if msg:
        assert output.message == msg


def test_when_not_exist_update_user_then_not_found(session):
    dto = UpdateUserDto(user_id=0)

    output = UpdateUserUseCase().execute(dto=dto)
    output.type = FailureType.NOT_FOUND_ERROR
