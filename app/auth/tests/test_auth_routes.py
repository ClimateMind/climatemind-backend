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
        base_frontend_url="https://app.climatemind.org",
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


def get_fake_registration_json():
    score = ScoresFactory()
    return {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "email": faker.email(),
        "password": faker.password(),
        "quizId": score.quiz_uuid,
    }
