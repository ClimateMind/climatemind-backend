from flask import url_for
import pytest

from app.factories import ScoresFactory


@pytest.mark.integration
def test_personal_values(client):
    score = ScoresFactory()
    response = client.get(
        url_for("personal_values.get_personal_values"),
        query_string={"quizId": score.quiz_uuid},
    )
    json = response.get_json()

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.access_control_allow_origin == "*"

    assert type(json) == dict
    assert "personalValues" in json
    assert "valueScores" in json

    assert type(json["personalValues"]) == list
    assert type(json["valueScores"]) == list

    assert len(json["personalValues"]) == 3
    assert len(json["valueScores"]) == 10

    for personal_value in json["personalValues"]:
        assert "id" in personal_value
        assert "description" in personal_value
        assert "shortDescription" in personal_value
        assert "name" in personal_value

    for value_score in json["valueScores"]:
        assert "personalValue" in value_score
        assert type(value_score["score"]) == float
        assert value_score["score"] >= 0
        assert value_score["score"] <= 10
