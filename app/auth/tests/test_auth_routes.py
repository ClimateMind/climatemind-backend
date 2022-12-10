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
    m_current_app.config.get.side_effect = (
        lambda key: "https://fake-url.local" if key == "BASE_FRONTEND_URL" else None
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


def get_fake_registration_json():
    score = ScoresFactory()
    return {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "email": faker.email(),
        "password": faker.password(),
        "quizId": score.quiz_uuid,
    }
