from flask import url_for
import pytest

from app.factories import ScoresFactory


@pytest.mark.integration
def test_post_code(client):
    score = ScoresFactory()
    response = client.post(
        url_for("post_code.post_code"),
        json={
            "postCode": score.postal_code,
            "quizId": score.quiz_uuid,
        },
    )
    json = response.get_json()

    assert response.status_code == 201
    assert response.content_type == "application/json"
    assert response.access_control_allow_origin == "*"

    assert type(json) == dict
    assert "message" in json
    assert "postCode" in json
    assert "quizId" in json
    assert type(json["quizId"]) == str


@pytest.mark.integration
def test_invalid_post_code(client):
    score = ScoresFactory()
    response = client.post(
        url_for("post_code.post_code"),
        json={
            "postCode": "123",
            "quizId": score.quiz_uuid,
        },
    )
    json = response.get_json()

    assert response.status_code == 400
    assert response.content_type == "application/json"
    assert response.access_control_allow_origin == "*"

    assert type(json) == dict
    assert "error" in json
    assert type(json["error"]) == str
    assert "The postcode provided is not valid." == json["error"]
