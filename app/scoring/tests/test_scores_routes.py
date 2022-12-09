import os.path
import pytest
from flask import url_for
from app.common.static import get_dict_from_json_file
from app.common.uuid import to_uuid

JSON_DIRECTORY = "app/scoring/tests/data"


@pytest.mark.integration
@pytest.mark.parametrize("json_file", [("postScores.json"), ("postScoresSetTwo.json")])
def test_post_scores(json_file, client_with_user_and_header, accept_json):
    client, _, session_header, _ = client_with_user_and_header
    url = url_for("scoring.user_scores")
    json = get_dict_from_json_file(os.path.join(JSON_DIRECTORY, json_file))
    response = client.post(
        url,
        headers=session_header + accept_json,
        json=json,
    )
    assert response.status_code == 201, "Posting scores must give HTTP 201"
    assert "quizId" in response.json.keys(), "Response must include quizId"
    assert to_uuid(response.json["quizId"]) is not None, "quizId must be a valid uuid"
