from flask import url_for

from core.domains.user.repository.user_repository import UserRepository


def test_when_signup_then_success(client, session, test_request_context, make_header):
    UserRepository().signup(nickname="test_nickname", password="test_password")

    headers = make_header()

    dct = dict(
        user_id=1,
        identification="test@email.com",
        type_="email",
    )

    with test_request_context:
        response = client.post(
            url_for("api.create_auth_view"), headers=headers, json=dct
        )

    assert response.status_code == 200
