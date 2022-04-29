from json import load

import pytest
from flask import url_for, current_app


@pytest.mark.integration
def test_get_questions(client):
    response = client.get(url_for("questions.get_questions"))
    json_file_name = current_app.config.get("SCHWARTZ_QUESTIONS_FILE")
    with open(json_file_name) as json_file:
        assert response.json == load(json_file)
