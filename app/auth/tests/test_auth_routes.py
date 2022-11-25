import pytest
from flask import url_for
from mock import mock

from app.common.tests.test_utils import get_sent_email_details, setup_sendgrid_mock
from app.factories import faker, ScoresFactory


@pytest.mark.integration
@mock.patch("app.sendgrid.utils.set_up_sendgrid")
def test_register_sends_welcome_email(m_set_up_sendgrid, client):
    sendgrid_mock = setup_sendgrid_mock(m_set_up_sendgrid)

    client.post(url_for("auth.register"), json=get_fake_registration_json())

    sendgrid_mock.send.assert_called_once()

    subject, substitutions = get_sent_email_details(sendgrid_mock)

    assert subject.startswith("Welcome")
    assert substitutions["-base_url-"] == "https://app.climatemind.org"


@pytest.mark.integration
@mock.patch("app.sendgrid.utils.current_app")
@mock.patch("app.sendgrid.utils.set_up_sendgrid")
def test_register_sends_welcome_email_with_configured_base_url(
    m_set_up_sendgrid, m_current_app, client
):
    m_current_app.config.get.side_effect = (
        lambda key: "https://fake-url.local" if key == "BASE_URL" else None
    )

    sendgrid_mock = setup_sendgrid_mock(m_set_up_sendgrid)

    client.post(url_for("auth.register"), json=get_fake_registration_json())

    sendgrid_mock.send.assert_called_once()

    subject, substitutions = get_sent_email_details(sendgrid_mock)

    assert subject.startswith("Welcome")
    assert substitutions["-base_url-"] == "https://fake-url.local"


def get_fake_registration_json():
    score = ScoresFactory()
    return {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "email": faker.email(),
        "password": faker.password(),
        "quizId": score.quiz_uuid,
    }
