from json import load

import pytest
from flask import url_for, current_app


@pytest.mark.integration
def test_get_questions(client):
    response = client.get(url_for("questions.get_questions"))

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.access_control_allow_origin == "*"

    json_decoded = response.get_json()
    assert type(json_decoded) == dict
    assert "SetOne" in json_decoded
    assert "SetTwo" in json_decoded
    assert "Answers" in json_decoded
    assert "Directions" in json_decoded


@pytest.mark.integration
def test_set_one_properties(client):
    response = client.get(url_for("questions.get_questions"))
    set_one = response.get_json()["SetOne"]

    assert isinstance(set_one, list)
    assert len(set_one) == 10
    for question_obj in set_one:
        assert type(question_obj) == dict
        assert "id" in question_obj
        assert "value" in question_obj
        assert "question" in question_obj
        assert type(question_obj["id"]) == int
        assert type(question_obj["value"]) == str
        assert type(question_obj["question"]) == str


@pytest.mark.integration
def test_set_two_properties(client):
    response = client.get(url_for("questions.get_questions"))
    set_two = response.get_json()["SetTwo"]

    assert isinstance(set_two, list)
    assert len(set_two) == 10
    for question_obj in set_two:
        assert type(question_obj) == dict
        assert "id" in question_obj
        assert "value" in question_obj
        assert "question" in question_obj
        assert type(question_obj["id"]) == int
        assert type(question_obj["value"]) == str
        assert type(question_obj["question"]) == str


@pytest.mark.integration
def test_answers_properties(client):
    response = client.get(url_for("questions.get_questions"))
    answers = response.get_json()["Answers"]

    assert isinstance(answers, list)
    assert len(answers) == 6
    for answer in answers:
        assert type(answer) == dict
        assert "id" in answer
        assert "text" in answer
        assert type(answer["id"]) == int
        assert type(answer["text"]) == str


@pytest.mark.integration
def test_directions_properties(client):
    response = client.get(url_for("questions.get_questions"))
    direction = response.get_json()["Directions"]

    assert type(direction) == str
    """
    json_file_name = current_app.config.get("SCHWARTZ_QUESTIONS_FILE")
    with open(json_file_name) as json_file:
        assert response.json == load(json_file)"""
