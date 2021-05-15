from flask import request
from flask_jwt_extended import jwt_required

from app.http.requests.user.v1.user_request import (
    SignupRequest,
    SigninRequest,
    UpdateUserRequest,
)
from app.http.responses import failure_response
from app.http.responses.presenters.user_presenter import (
    SignupPresenter,
    SigninPresenter,
    UpdateUserPresenter,
)
from app.http.view import api
from app.http.view.auth import auth_required, current_user

from core.domains.user.use_case.signin_use_case import SigninUseCase
from core.domains.user.use_case.signup_use_case import SignupUseCase
from core.domains.user.use_case.update_user_use_case import UpdateUserUseCase
from core.use_case_output import UseCaseFailureOutput, FailureType


@api.route("/user/v1/signup", methods=["POST"])
def signup_view():
    dto = SignupRequest(**request.get_json()).validate_request_and_make_dto()
    if not dto:
        return failure_response(
            UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)
        )

    return SignupPresenter().transform(SignupUseCase().execute(dto=dto))


@api.route("/user/v1/signin", methods=["POST"])
def signin_view():
    dto = SigninRequest(**request.get_json()).validate_request_and_make_dto()
    if not dto:
        return failure_response(
            UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)
        )

    return SigninPresenter().transform(SigninUseCase().execute(dto=dto))


@api.route("/user/v1/user/<int:user_id>", methods=["PUT"])
@jwt_required()
@auth_required
def update_user_view(user_id):
    dto = UpdateUserRequest(
        **request.get_json(), user_id=current_user.id
    ).validate_request_and_make_dto()
    if not dto:
        return failure_response(
            UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)
        )

    return UpdateUserPresenter().transform(UpdateUserUseCase().execute(dto=dto))
