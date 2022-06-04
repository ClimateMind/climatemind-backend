import pytest
from flask import url_for
from flask_jwt_extended import create_access_token
from mock import mock

from app.factories import UsersFactory, faker


@pytest.mark.integration
def test_current_email(client):
    user = UsersFactory()

    with mock.patch("flask_jwt_extended.utils.get_current_user", return_value=user):
        response = client.get(url_for("account.current_email"))
        assert response.status_code == 401, "Unauthorized request"

        access_token = create_access_token(identity=user, fresh=True)
        client.set_cookie("localhost", "access_token", access_token)
        response = client.get(url_for("account.current_email"))
        assert response.status_code == 200, "Is success"
        assert response.json.get("currentEmail") == user.user_email


@pytest.mark.integration
def test_update_email(client, accept_json):
    response = client.put(url_for("account.update_email"), headers=accept_json)
    assert response.status_code == 401, "Unauthorized request"

    password = faker.password()
    user = UsersFactory(password=password)

    access_token = create_access_token(identity=user, fresh=True)
    client.set_cookie("localhost", "access_token", access_token)
    new_email = faker.email()

    response = client.put(
        url_for("account.update_email"),
        headers=accept_json,
        json={
            "password": password,
            "confirmEmail": new_email,
            "newEmail": new_email,
        },
    )
    assert response.status_code == 200, "Email changed successfully"

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

    weak_password = "password"
    response = client.put(
        url,
        headers=headers,
        json={
            "currentPassword": current_password,
            "newPassword": weak_password,
            "confirmPassword": weak_password,
        },
    )
    assert response.status_code == 422, "Weak password provided"
    assert not user.check_password(weak_password)

    response = client.put(
        url,
        headers=headers,
        json={
            "currentPassword": current_password,
            "newPassword": new_password,
            "confirmPassword": new_password + "312",
        },
    )
    assert response.status_code == 422, "Password mismatch"
    assert not user.check_password(new_password)

    response = client.put(
        url,
        headers=headers,
        json={
            "currentPassword": current_password,
            "newPassword": new_password,
            "confirmPassword": new_password,
        },
    )
    assert response.status_code == 200, "Password changed successfully"
    assert user.check_password(new_password)
