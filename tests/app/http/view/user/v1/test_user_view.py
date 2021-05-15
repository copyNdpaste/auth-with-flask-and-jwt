from flask import url_for

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
