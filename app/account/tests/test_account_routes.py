from datetime import datetime, timedelta

from time import sleep
import pytest
import typing
from flask import url_for
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from freezegun import freeze_time
from mock import mock

from app.factories import UsersFactory, faker, SessionsFactory, PasswordResetLinkFactory
from app.models import PasswordResetLink, Users


@pytest.mark.integration
def test_current_email(client):
    user = UsersFactory()

    with mock.patch("flask_jwt_extended.utils.get_current_user", return_value=user):

        response = client.get(url_for("account.current_email"))
        assert response.status_code == 401, "Unauthorized request"
        assert response.json == {
            "msg": 'Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token")'
        }

        expiry_milliseconds = 1.0
        access_token = create_access_token(
            identity=user,
            fresh=True,
            expires_delta=timedelta(milliseconds=expiry_milliseconds),
        )
        client.set_cookie("localhost", "access_token", access_token)
        sleep(0.001 * expiry_milliseconds)
        response = client.get(url_for("account.current_email"))
        assert response.status_code == 401, "Unauthorized request"
        assert response.json == {"msg": "Token has expired"}

        access_token = create_access_token(
            identity=user, fresh=True, expires_delta=timedelta(seconds=60)
        )
        client.set_cookie("localhost", "access_token", access_token)
        response = client.get(url_for("account.current_email"))
        assert response.status_code == 200, "Is success"
        assert response.json.get("currentEmail") == user.user_email


@pytest.mark.integration
def test_update_email(client, accept_json):
    password = faker.password()
    user = UsersFactory(password=password)
    old_email = user.user_email
    new_email = faker.email()
    ok_data = {
        "password": password,
        "confirmEmail": new_email,
        "newEmail": new_email,
    }

    response = client.put(
        url_for("account.update_email"), headers=accept_json, json=ok_data
    )
    assert response.status_code == 401, "Unauthorized request"
    assert response.json == {
        "msg": 'Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token")'
    }
    assert user.user_email == old_email

    expiry_milliseconds = 1.0
    access_token = create_access_token(
        identity=user,
        fresh=True,
        expires_delta=timedelta(milliseconds=expiry_milliseconds),
    )
    client.set_cookie("localhost", "access_token", access_token)
    sleep(0.001 * expiry_milliseconds)
    response = client.put(
        url_for("account.update_email"), headers=accept_json, json=ok_data
    )
    assert response.status_code == 401, "Unauthorized request"
    assert response.json == {"msg": "Token has expired"}
    assert user.user_email == old_email

    access_token = create_access_token(
        identity=user, fresh=True, expires_delta=timedelta(hours=1)
    )
    client.set_cookie("localhost", "access_token", access_token)
    response = client.put(
        url_for("account.update_email"), headers=accept_json, json=ok_data
    )
    assert response.status_code == 200, "Email changed successfully"
    assert user.user_email == new_email

    response_login_with_old_email = client.post(
        url_for("auth.login"),
        json={
            "email": old_email,
            "password": password,
        },
    )
    assert (
        response_login_with_old_email.status_code == 401
    ), "Login with old email denied"
    assert response_login_with_old_email.json == {
        "error": "Wrong email or password. Try again."
    }

    response_login_with_new_email = client.post(
        url_for("auth.login"),
        json={
            "email": new_email,
            "password": password,
        },
    )
    assert (
        response_login_with_new_email.status_code == 200
    ), "Login with new email successful"

    response = client.put(
        url_for("account.update_email"),
        headers=accept_json,
        json={
            "password": password,
            "confirmEmail": new_email,
            "newEmail": new_email,
        },
    )
    assert response.status_code == 409, "Cannot change email to itself"
    assert response.json == {
        "error": "Cannot update email. Email already exists in the database."
    }

    response = client.put(
        url_for("account.update_email"),
        headers=accept_json,
        json={
            # "password": password,
            "confirmEmail": new_email,
            "newEmail": new_email,
        },
    )
    assert response.status_code == 400, "Password is required"
    assert response.json == {"error": "password must be included in the request body."}

    response = client.put(
        url_for("account.update_email"),
        headers=accept_json,
        json={
            "password": password,
            # "confirmEmail": new_email,
            "newEmail": new_email,
        },
    )
    assert response.status_code == 400, "Confirm email is required"
    assert response.json == {
        "error": "confirmEmail must be included in the request body."
    }

    response = client.put(
        url_for("account.update_email"),
        headers=accept_json,
        json={
            "password": password,
            "confirmEmail": new_email,
            # "newEmail": new_email,
        },
    )
    assert response.status_code == 400, "New email is required"
    assert response.json == {"error": "newEmail must be included in the request body."}

    invalid_email = "invalid,@email"
    response = client.put(
        url_for("account.update_email"),
        headers=accept_json,
        json={
            "password": password,
            "confirmEmail": invalid_email,
            "newEmail": invalid_email,
        },
    )
    assert response.status_code == 400, "Email is invalid"
    assert response.json == {
        "error": "Cannot update email. Email is not formatted correctly."
    }

    response = client.put(
        url_for("account.update_email"),
        headers=accept_json,
        json={
            "password": "Wrong" + password,
            "confirmEmail": new_email,
            "newEmail": new_email,
        },
    )
    assert response.status_code == 401, "Wrong password"
    assert response.json == {"error": "Cannot update email. Incorrect password."}

    response = client.put(
        url_for("account.update_email"),
        headers=accept_json,
        json={
            "password": password,
            "confirmEmail": new_email + "with typo",
            "newEmail": new_email,
        },
    )
    assert response.status_code == 400, "Emails should be equal"
    assert response.json == {
        "error": "Cannot update email. New email address and confirm new email address do not match."
    }

    another_user = UsersFactory()
    response = client.put(
        url_for("account.update_email"),
        headers=accept_json,
        json={
            "password": password,
            "confirmEmail": another_user.user_email,
            "newEmail": another_user.user_email,
        },
    )
    assert response.status_code == 409, "Email is not unique"
    assert response.json == {
        "error": "Cannot update email. Email already exists in the database."
    }


@pytest.mark.integration
def test_update_user_account(client_with_user_and_header, accept_json):
    client, user, session_header, current_password = client_with_user_and_header
    new_password = faker.password()

    url = url_for("account.update_user_account")
    headers = session_header + accept_json

    invalid_password = "wrong_password"
    response = client.put(
        url,
        headers=headers,
        json={
            "currentPassword": invalid_password,
            "newPassword": new_password,
            "confirmPassword": new_password,
        },
    )
    assert response.status_code == 403, "Wrong password provided"
    assert not user.check_password(new_password)

    default_data = {"currentPassword": current_password}
    update_password_checks(client, headers, new_password, url, user, default_data)


def update_password_checks(
    client: FlaskClient,
    headers: list,
    new_password: str,
    url: str,
    user: Users,
    default_data: typing.Optional[dict] = None,
):
    weak_password = "password"
    data = default_data if default_data else {}
    data.update(
        {
            "newPassword": weak_password,
            "confirmPassword": weak_password,
        }
    )
    response = client.put(url, headers=headers, json=data)
    assert response.status_code == 422, "Weak password provided"
    assert not user.check_password(weak_password), "Password wasn't updated"

    data = default_data if default_data else {}
    data.update(
        {
            "newPassword": new_password,
            "confirmPassword": new_password + "312",
        }
    )
    response = client.put(url, headers=headers, json=data)
    assert response.status_code == 422, "Password mismatch"
    assert not user.check_password(new_password), "Password wasn't updated"

    data = default_data if default_data else {}
    data.update(
        {
            "newPassword": new_password,
        }
    )
    response = client.put(url, headers=headers, json=data)
    assert response.status_code == 422, "Field missing"
    assert not user.check_password(new_password), "Password wasn't updated"

    data = default_data if default_data else {}
    data.update(
        {
            "newPassword": new_password,
            "confirmPassword": new_password,
        }
    )
    response = client.put(url, headers=headers, json=data)
    assert response.status_code == 200, "Password changed successfully"
    assert user.check_password(new_password), "Password was finally updated"


@pytest.mark.integration
@mock.patch("app.account.routes.send_reset_password_email")
def test_create_and_send_password_reset_link_email(
    m_send_reset_password_email, client, accept_json
):
    session = SessionsFactory()
    session_header = [("X-Session-Id", session.session_uuid)]

    url = url_for("account.create_and_send_password_reset_link_email")
    not_registered_email = faker.email()

    response = client.post(
        url,
        headers=session_header,
        json={
            "email": not_registered_email,
        },
    )
    assert response.status_code == 200, "Status should be 200 in security reasons"
    assert PasswordResetLink.query.count() == 0
    assert not m_send_reset_password_email.called

    user = UsersFactory()
    registered_email = user.user_email

    response = client.post(
        url,
        headers=session_header,
        json={
            "email": registered_email,
        },
    )
    assert response.status_code == 200, "Success"
    assert PasswordResetLink.query.count() == 1, "Single object should be created"

    password_reset = PasswordResetLink.query.first()
    assert password_reset.user == user, "User is correct"
    assert m_send_reset_password_email.called_once_with(
        registered_email, password_reset.reset_url, password_reset.EXPIRE_HOURS_COUNT
    ), "Email was sent with the correct parameters."

    response = client.post(
        url,
        headers=session_header,
        json={
            "email": registered_email,
        },
    )
    assert response.status_code == 200, "Success"
    assert PasswordResetLink.query.count() == 2, "Second object should be created"


@pytest.mark.integration
def test_do_password_reset(client, accept_json):
    session = SessionsFactory()
    session_header = [("X-Session-Id", session.session_uuid)]
    new_password = faker.password()
    password_reset = PasswordResetLinkFactory()

    url = url_for(
        "account.do_password_reset", password_reset_link_uuid=password_reset.uuid
    )

    update_password_checks(
        client, session_header, new_password, url, password_reset.user
    )


faked_now = faker.date_time()


@freeze_time(faked_now)
@pytest.mark.integration
def test_check_if_password_reset_link_is_expired(client, accept_json):
    session = SessionsFactory()
    session_header = [("X-Session-Id", session.session_uuid)]

    big_value_to_make_sure_the_password_reset_object_is_expired_already = 999
    password_reset_expired = PasswordResetLinkFactory(
        created=datetime.now()
        - timedelta(
            hours=big_value_to_make_sure_the_password_reset_object_is_expired_already
        )
    )

    url = url_for(
        "account.check_if_password_reset_link_is_expired_or_used",
        password_reset_link_uuid=password_reset_expired.uuid,
    )
    response = client.get(url, headers=session_header)
    assert response.status_code == 410, "Expired"


@pytest.mark.integration
def test_check_if_password_reset_link_is_used(client, accept_json):
    session = SessionsFactory()
    session_header = [("X-Session-Id", session.session_uuid)]

    password_reset = PasswordResetLinkFactory()

    check_if_link_is_valid_url = url_for(
        "account.check_if_password_reset_link_is_expired_or_used",
        password_reset_link_uuid=password_reset.uuid,
    )
    response = client.get(check_if_link_is_valid_url, headers=session_header)
    assert response.status_code == 200, "Fresh link is ready to use"

    new_password = faker.password()
    response = client.put(
        url_for(
            "account.do_password_reset", password_reset_link_uuid=password_reset.uuid
        ),
        headers=session_header,
        json={
            "newPassword": new_password,
            "confirmPassword": new_password,
        },
    )
    assert response.status_code == 200, "Password changed successfully"
    assert password_reset.user.check_password(new_password), "Password was updated"

    check_if_link_is_valid_url = url_for(
        "account.check_if_password_reset_link_is_expired_or_used",
        password_reset_link_uuid=password_reset.uuid,
    )
    response = client.get(check_if_link_is_valid_url, headers=session_header)
    assert response.status_code == 409, "Is used already"
