from flask import url_for
import pytest

from app.common.tests.utils import is_none_or_type

actions_effect_name = "increase in flooding of land and property"


@pytest.mark.integration
def test_solutions(client):
    response = client.get(url_for("solutions.get_general_solutions"))
    json = response.get_json()

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.access_control_allow_origin == "*"

    assert type(json) == dict
    assert "solutions" in json
    assert type(json["solutions"]) == list


@pytest.mark.integration
def test_solution_properties(client):
    response = client.get(url_for("solutions.get_general_solutions"))
    json = response.get_json()
    solutions = json["solutions"]

    assert len(solutions) > 0
    for solution in solutions:
        assert_solution_or_action_properties(solution)
        assert "solutionCo2EqReduced" in solution
        assert is_none_or_type(solution["solutionCo2EqReduced"], float)


def test_get_actions(client):
    response = client.get(
        url_for("solutions.get_actions"),
        query_string={"effect-name": actions_effect_name},
    )
    json = response.get_json()

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.access_control_allow_origin == "*"

    assert type(json) == dict
    assert "actions" in json
    assert type(json["actions"]) == list
    assert len(json["actions"]) != 0


@pytest.mark.integration
def test_get_actions_properties(client):
    response = client.get(
        url_for("solutions.get_actions"),
        query_string={"effect-name": actions_effect_name},
    )
    json = response.get_json()
    actions = json["actions"]

    assert len(actions) > 0
    for action in actions:
        assert_solution_or_action_properties(action)


def assert_solution_or_action_properties(solution_or_action):
    assert type(solution_or_action) == dict

    assert "imageUrl" in solution_or_action
    assert "iri" in solution_or_action
    assert "longDescription" in solution_or_action
    assert "shortDescription" in solution_or_action
    assert "solutionSources" in solution_or_action
    assert "solutionSpecificMythIRIs" in solution_or_action
    assert "solutionTitle" in solution_or_action
    assert "solutionType" in solution_or_action

    assert is_none_or_type(solution_or_action["imageUrl"], str)
    assert type(solution_or_action["iri"]) == str
    assert type(solution_or_action["longDescription"]) == str
    assert type(solution_or_action["shortDescription"]) == str
    assert type(solution_or_action["solutionSources"]) == list
    assert type(solution_or_action["solutionSpecificMythIRIs"]) == list
    assert type(solution_or_action["solutionTitle"]) == str
    assert type(solution_or_action["solutionType"]) == str

    for solutionSource in solution_or_action["solutionSources"]:
        assert type(solutionSource) == str

    for solutionSpecificMythIRI in solution_or_action["solutionSpecificMythIRIs"]:
        assert type(solutionSpecificMythIRI) == str
