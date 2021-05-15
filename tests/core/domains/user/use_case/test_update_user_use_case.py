import pytest

from core.domains.user.dto.user_dto import UpdateUserDto
from core.domains.user.repository.user_repository import UserRepository
from core.domains.user.use_case.update_user_use_case import UpdateUserUseCase
from core.use_case_output import FailureType, UseCaseSuccessOutput


@pytest.mark.parametrize(
    "nickname, new_nickname, current_password, current_password_check, new_password, result",
    [
        (
            "test_nickname",
            "new_nickname",
            "test_password",
            "test_password",
            "new_password",
            True,
        ),
        ("test_nickname", None, "test_password", "test_password", "new_password", True),
        (
            "test_nickname",
            None,
            "test_password",
            "test_passwor",
            "new_password",
            FailureType.INVALID_REQUEST_ERROR,
        ),
        (
            "test_nickname",
            None,
            "test_passwor",
            "test_password",
            "new_password",
            FailureType.INVALID_REQUEST_ERROR,
        ),
        (
            "test_nickname",
            None,
            "test_password",
            "test_password",
            "test_password",
            FailureType.INVALID_REQUEST_ERROR,
        ),
        (
            "test_nickname",
            None,
            "test_passwor",
            "test_password",
            None,
            FailureType.INVALID_REQUEST_ERROR,
        ),
    ],
)
def test_when_update_user(
    session,
    nickname,
    new_nickname,
    current_password,
    current_password_check,
    new_password,
    result,
):
    UserRepository().signup(nickname=nickname, password=current_password)

    dto = UpdateUserDto(
        user_id=1,
        nickname=nickname,
        new_nickname=new_nickname,
        current_password=current_password,
        current_password_check=current_password_check,
        new_password=new_password,
    )

    output = UpdateUserUseCase().execute(dto=dto)
    if isinstance(output, UseCaseSuccessOutput):
        assert output.value == result
        user = UserRepository().get_user(user_id=1)
        assert user.nickname is not None
    else:
        assert output.type == result
