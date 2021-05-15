from flask import url_for
from flask_jwt_extended import create_access_token

from core.domains.user.repository.user_repository import UserRepository


def test_when_signup_then_success(client, session, test_request_context, make_header):
    nickname = "test_nickname"
    password = "test_password"

    headers = make_header()

    dct = dict(nickname=nickname, password=password)

    with test_request_context:
        response = client.post(url_for("api.signup_view"), headers=headers, json=dct)

    assert response.status_code == 200


def test_when_signin_then_success(client, session, test_request_context, make_header):
    nickname = "test_nickname"
    password = "test_password"

    UserRepository().signup(nickname=nickname, password=password)

    headers = make_header()

    dct = dict(nickname=nickname, password=password)

    with test_request_context:
        response = client.post(url_for("api.signin_view"), headers=headers, json=dct)

    assert response.status_code == 200
    assert isinstance(response.get_json()["data"], str)


def test_when_update_user_then_success(
    client, session, test_request_context, make_header, jwt_manager
):
    nickname = "test_nickname"
    password = "test_password"

    UserRepository().signup(nickname=nickname, password=password)

    authorization = "Bearer " + create_access_token(identity=1)
    headers = make_header(authorization=authorization)

    dct = dict(new_nickname="new_nickname")

    with test_request_context:
        response = client.put(
            url_for("api.update_user_view", user_id=1), headers=headers, json=dct
        )

    assert response.status_code == 200
    assert response.get_json()["data"] == True
