from flask import request

from app.http.requests.user.v1.user_request import SignupRequest
from app.http.responses import failure_response
from app.http.responses.presenters.user_presenter import SignupPresenter
from app.http.view import api

from core.domains.user.use_case.signup_use_case import SignupUseCase
from core.use_case_output import UseCaseFailureOutput, FailureType


@api.route("/user/v1/signup", methods=["POST"])
def signup_view():
    dto = SignupRequest(**request.get_json()).validate_request_and_make_dto()
    if not dto:
        return failure_response(
            UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)
        )

    return SignupPresenter().transform(SignupUseCase().execute(dto=dto))
