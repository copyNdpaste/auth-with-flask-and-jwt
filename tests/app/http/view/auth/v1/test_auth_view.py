from datetime import timedelta

from flask import url_for

from app.extensions.utils.time_helper import get_utc_timestamp
from core.domains.user.repository.auth_repository import AuthRepository
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


def test_when_verify_auth_then_success(
    client, session, test_request_context, make_header
):
    UserRepository().signup(nickname="test_nickname", password="test_password")
    AuthRepository().create_auth(
        user_id=1,
        identification="test@email.com",
        type_="email",
        verify_code="1234",
        expired_at=get_utc_timestamp() + timedelta(minutes=3),
    )

    headers = make_header()

    dct = dict(
        user_id=1,
        identification="test@email.com",
        verify_code="1234",
    )

    with test_request_context:
        response = client.put(
            url_for("api.verify_auth_view"), headers=headers, json=dct
        )

    assert response.status_code == 200
