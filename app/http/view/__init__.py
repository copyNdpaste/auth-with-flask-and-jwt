from flask import Blueprint


api: Blueprint = Blueprint(name="api", import_name=__name__)

from .auth.v1.auth_view import *  # noqa isort:skip
from .user.v1.user_view import *  # noqa isort:skip
