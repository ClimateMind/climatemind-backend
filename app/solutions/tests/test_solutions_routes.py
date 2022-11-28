from flask import url_for
import pytest

from app.common.tests.utils import is_none_or_type


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
        assert type(solution) == dict

        assert "imageUrl" in solution
        assert "iri" in solution
        assert "longDescription" in solution
        assert "shortDescription" in solution
        assert "solutionCo2EqReduced" in solution
        assert "solutionSources" in solution
        assert "solutionSpecificMythIRIs" in solution
        assert "solutionTitle" in solution
        assert "solutionType" in solution

        assert is_none_or_type(solution["imageUrl"], str)
        assert is_none_or_type(solution["solutionCo2EqReduced"], float)
        assert type(solution["iri"]) == str
        assert type(solution["longDescription"]) == str
        assert type(solution["shortDescription"]) == str
        assert type(solution["solutionSources"]) == list
        assert type(solution["solutionSpecificMythIRIs"]) == list
        assert type(solution["solutionTitle"]) == str
        assert type(solution["solutionType"]) == str

        for solutionSource in solution["solutionSources"]:
            assert type(solutionSource) == str

        for solutionSpecificMythIRI in solution["solutionSpecificMythIRIs"]:
            assert type(solutionSpecificMythIRI) == str
