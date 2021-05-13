from flask import url_for


def test_when_signup_then_success(client, session, test_request_context, make_header):
    nickname = "test_nickname"
    password = "test_password"

    headers = make_header()

    dct = dict(nickname=nickname, password=password)

    with test_request_context:
        response = client.post(url_for("api.signup_view"), headers=headers, json=dct)

    assert response.status_code == 200
