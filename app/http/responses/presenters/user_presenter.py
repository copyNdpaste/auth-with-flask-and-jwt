from typing import Union

from app.extensions.utils.log_helper import logger_
from app.http.responses import failure_response, success_response

from core.use_case_output import UseCaseSuccessOutput, UseCaseFailureOutput

logger = logger_.getLogger(__name__)


class SignupPresenter:
    def transform(self, output: Union[UseCaseSuccessOutput, UseCaseFailureOutput]):
        if isinstance(output, UseCaseSuccessOutput):
            value = output.value
            result = {
                "data": value,
                "meta": output.meta,
            }
            return success_response(result=result)
        elif isinstance(output, UseCaseFailureOutput):
            return failure_response(output=output)


class SigninPresenter:
    def transform(self, output: Union[UseCaseSuccessOutput, UseCaseFailureOutput]):
        if isinstance(output, UseCaseSuccessOutput):
            value = output.value
            result = {
                "data": value,
                "meta": output.meta,
            }
            return success_response(result=result)
        elif isinstance(output, UseCaseFailureOutput):
            return failure_response(output=output)


class UpdateUserPresenter:
    def transform(self, output: Union[UseCaseSuccessOutput, UseCaseFailureOutput]):
        if isinstance(output, UseCaseSuccessOutput):
            value = output.value
            result = {
                "data": value,
                "meta": output.meta,
            }
            return success_response(result=result)
        elif isinstance(output, UseCaseFailureOutput):
            return failure_response(output=output)
