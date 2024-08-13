import pytest
from flask import url_for
from mock import mock

from app.common.tests.utils import assert_email_sent
from app.factories import faker, ScoresFactory


@pytest.mark.integration
def test_register_sends_welcome_email(sendgrid_mock, client):
    client.post(url_for("auth.register"), json=get_fake_registration_json())

    assert_email_sent(
        sendgrid_mock,
        subject_starts_with="Welcome",
        base_frontend_url="http://localhost:3000",
    )


@pytest.mark.integration
@mock.patch("app.sendgrid.utils.current_app")
def test_register_sends_welcome_email_with_configured_base_frontend_url(
    m_current_app, sendgrid_mock, client
):
    m_current_app.config.get.side_effect = lambda key: (
        "https://fake-url.local" if key == "BASE_FRONTEND_URL" else None
    )

    client.post(url_for("auth.register"), json=get_fake_registration_json())

    assert_email_sent(
        sendgrid_mock,
        subject_starts_with="Welcome",
        base_frontend_url="https://fake-url.local",
    )


@pytest.mark.integration
@mock.patch("app.auth.routes.unset_jwt_cookies")
def test_logout(m_unset_jwt_cookies, client):
    response = client.post(url_for("auth.logout"))
    json = response.get_json()

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.access_control_allow_origin == "http://0.0.0.0:3000"

    assert type(json) == dict
    assert "message" in json
    assert type(json["message"]) == str
    assert json["message"] == "User logged out"

    m_unset_jwt_cookies.assert_called_once()


@pytest.mark.integration
def test_successful_registry_basic(client):
    data = get_fake_registration_json()
    response = client.post(url_for("auth.register"), json=data)
    assert response.status_code == 201
    header_map = {name.lower(): value.lower() for (name, value) in response.headers}
    assert header_map["access-control-allow-origin"] == "http://0.0.0.0:3000"
    assert header_map["content-type"] == "application/json"
    assert isinstance(response.json, dict), "Response must be a dict"
    assert (
        response.json["message"] == "Successfully created user"
    ), "Response must have appropriate message"


@pytest.mark.integration
def test_successful_registry_second_user(client):
    client.post(
        url_for("auth.register", json=get_fake_registration_json())
    )  # first user
    response = client.post(
        url_for("auth.register"), json=get_fake_registration_json()
    )  # another user
    assert response.status_code == 201
    header_map = {name.lower(): value.lower() for (name, value) in response.headers}
    assert header_map["access-control-allow-origin"] == "http://0.0.0.0:3000"
    assert header_map["content-type"] == "application/json"
    assert isinstance(response.json, dict), "Response must be a dict"
    assert (
        response.json["message"] == "Successfully created user"
    ), "Response must have appropriate success message"


@pytest.mark.parametrize(
    "missing_field",
    [
        "firstName",
        "lastName",
        "email",
        "password",
        "quizId",
    ],
)
@pytest.mark.integration
def test_failed_registry_missing_field(missing_field, client):
    data = get_fake_registration_json()
    data.pop(missing_field)
    response = client.post(url_for("auth.register"), json=data)
    assert response.status_code == 400
    header_map = {name.lower(): value.lower() for (name, value) in response.headers}
    assert header_map["content-type"] == "application/json"
    assert response.json == {
        "error": "{} must be included in the request body.".format(missing_field)
    }


@pytest.mark.integration
def test_failed_registry_missing_body(client):
    response = client.post(url_for("auth.register"))
    assert response.status_code == 400
    header_map = {name.lower(): value.lower() for (name, value) in response.headers}
    assert header_map["content-type"] == "application/json"
    assert response.json == {"error": "JSON body must be included in the request."}


@pytest.mark.integration
def test_failed_registry_reregistry(client):
    data = get_fake_registration_json()
    client.post(url_for("auth.register"), json=data)  # first registry
    response = client.post(url_for("auth.register"), json=data)  # reregistry attempt
    assert response.status_code == 409
    header_map = {name.lower(): value.lower() for (name, value) in response.headers}
    assert header_map["content-type"] == "application/json"
    assert response.json == {
        "error": "Cannot register email. Email already exists in the database."
    }, "Response must have appropriate error message"


recaptcha_Token = "03AGdBq27Tmja4W082LAEVoYyuuALGQwMVxOuOGDduLCQSTWWFuTtc4hQsc-KUVhsJQlBzEjdtxTqs1kXHusJCk2husZjY44rA-opJLWOgJuVUIoGtXozHtYhtmR5DibuJ3idGLalZ00niqnaa0zHC73hWPzc1CtnUO258nZLh1uxePi7DI-afWQd6aa4-EuRcPabG_E500r9S4RReTg42WtP8SNrqEdFoG9UdPoIF2aGCArHD6GqhQzwOev8_jeKUzcxq_1wEvxiID2ow7rxK339PCeTgO9Zz9fPnhTZ6mKaa_tmL1bSQ2zvWvA0Z5An3YvMP3sureZVR_mhJP2r84sYw9WbuI6hRr1oUGtTGuACB-IBqqE5m-meetr870N2Gl-vp3veeEyo34HLj5iDOr6YwyIXWBKam7mDHfhjps1QeiN90291e6CxaFd-bOkeazZyu2_aEPblNwIiUBl0BobqJ2dT2HlxXCRma0QDuX4xLvwh8_ayrJGo9t6nRxQHghZ2ZEh450bM0bVFAqkIGAqYv_EvYj7_XgQ"  # this is the string from the cypress test I'm replacing ...
recaptcha_Token = "abcdef"  # ... but any string works!


@pytest.mark.integration
@mock.patch("app.auth.routes.check_if_local")
def test_successful_login(m_check_if_local, client):
    m_check_if_local.return_value = True  # to test for recaptchaToken
    registration = get_fake_registration_json()
    client.post(url_for("auth.register"), json=registration).json["user"]

    response = client.post(
        url_for("auth.login"),
        json={
            "email": registration["email"],
            "password": registration["password"],
            "recaptchaToken": recaptcha_Token,
        },
    )
    assert response.status_code == 200, "Successful login"

    header_map = {name.lower(): value.lower() for (name, value) in response.headers}
    assert header_map["content-type"] == "application/json", "content-type is json"
    assert header_map["access-control-allow-origin"] == "http://0.0.0.0:3000"

    assert isinstance(response.json, dict), "response is a dict"

    assert "message" in response.json.keys(), "response has a message"
    assert isinstance(response.json["message"], str), "response message is a string"

    assert "access_token" in response.json.keys(), "response has an access_token"
    assert isinstance(
        response.json["access_token"], str
    ), "response access_token is a string"

    assert "user" in response.json.keys(), "response has a user"
    assert isinstance(response.json["user"], dict), "response user is a dict"
    assert isinstance(
        response.json["user"]["first_name"], str
    ), "response user first_name is a string"
    assert isinstance(
        response.json["user"]["last_name"], str
    ), "response user last_name is a string"
    assert isinstance(
        response.json["user"]["email"], str
    ), "response user email is a string"
    assert isinstance(
        response.json["user"]["user_uuid"], str
    ), "response user uuid is a string"
    print(response.json["user"]["quiz_id"])
    assert isinstance(
        response.json["user"]["quiz_id"], str
    ), "response user quiz id {} is not a string".format(
        response.json["user"]["quiz_id"]
    )


@pytest.mark.integration
@pytest.mark.parametrize(
    "data",  # interpret None field as missing field, and no field as registration value
    [
        {"email": None, "password": None},
        {"email": None},
        {"password": None},
        {"email": faker.email()},
        {"password": faker.password()},
    ],
)
def test_failed_login(data, client):
    registration = get_fake_registration_json()
    client.post(url_for("auth.register"), json=registration).json["user"]

    status_code = 401
    for key in ["email", "password"]:
        if key not in data:
            data[key] = registration[key]
        elif data[key] is None:
            status_code = 400
    if status_code == 400:
        message = "Email and password must be included in the request body."
    elif status_code == 401:
        message = "Wrong email or password. Try again."

    response = client.post(
        url_for("auth.login"),
        json={
            "email": data["email"],
            "password": data["password"],
        },
    )

    assert response.status_code == status_code, ("Failed login", response.status_code)
    header_map = {name.lower(): value.lower() for (name, value) in response.headers}
    assert header_map["content-type"] == "application/json"
    assert response.json == {"error": message}, "Expected error message"


def get_fake_registration_json():
    score = ScoresFactory()
    return {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "email": faker.email(),
        "password": faker.password(),
        "quizId": score.quiz_uuid,
    }
