import pytest
from flask import url_for

from app.factories import faker, SessionsFactory
from app.models import Feedback


@pytest.mark.integration
@pytest.mark.parametrize(
    "data, code",
    (
        ({"text": faker.text(max_nb_chars=2000)}, 200),
        ({"text": faker.text(max_nb_chars=5000)}, 422),
        ({"feedback": faker.text()}, 422),
        ({"text": faker.text(), "wrong": 123}, 422),
        ({}, 422),
    ),
)
def test_post_feedback(data, code, client, accept_json):
    session = SessionsFactory()
    session_header = [("X-Session-Id", session.session_uuid)]

    assert Feedback.query.count() == 0
    url = url_for("feedback.post_feedback")
    response = client.post(url, headers=session_header, json=data)
    assert response.status_code == code, response.data

    if code == 200:
        assert Feedback.query.count() == 1
        feedback = Feedback.query.first()
        assert data["text"] <= feedback.text
    else:
        assert Feedback.query.count() == 0
