from flask import request

from app.http.requests.auth.v1.auth_request import CreateAuthRequest
from app.http.responses import failure_response
from app.http.responses.presenters.auth_presenter import CreateAuthPresenter
from app.http.view import api

from core.domains.auth.use_case.create_auth_use_case import CreateAuthUseCase
from core.use_case_output import UseCaseFailureOutput, FailureType


@api.route("/auth/v1", methods=["POST"])
def create_auth_view():
    dto = CreateAuthRequest(**request.get_json()).validate_request_and_make_dto()
    if not dto:
        return failure_response(
            UseCaseFailureOutput(type=FailureType.INVALID_REQUEST_ERROR)
        )

    return CreateAuthPresenter().transform(CreateAuthUseCase().execute(dto=dto))
