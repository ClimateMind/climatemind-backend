from flask import url_for
import pytest

from app.common.tests.utils import is_none_or_type
from app.factories import ScoresFactory


@pytest.mark.integration
def test_feed(client_with_user_and_header):
    client, _, session_header, _ = client_with_user_and_header
    score = ScoresFactory()
    response = client.get(
        url_for("scoring.get_feed"),
        headers=session_header,
        query_string={"quizId": score.quiz_uuid},
    )
    json = response.get_json()

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.access_control_allow_origin == "*"

    assert type(json) == dict
    assert "climateEffects" in json
    assert type(json["climateEffects"]) == list


@pytest.mark.integration
def test_feed_properties(client_with_user_and_header):
    client, _, session_header, _ = client_with_user_and_header
    score = ScoresFactory()
    response = client.get(
        url_for("scoring.get_feed"),
        headers=session_header,
        query_string={"quizId": score.quiz_uuid},
    )
    json = response.get_json()

    assert len(json["climateEffects"]) > 0
    for climate_effect in json["climateEffects"]:
        assert type(climate_effect) == dict

        assert "effectDescription" in climate_effect
        assert "effectId" in climate_effect
        assert "effectScore" in climate_effect
        assert "effectShortDescription" in climate_effect
        assert "effectSolutions" in climate_effect
        assert "effectSources" in climate_effect
        assert "effectSpecificMythIRIs" in climate_effect
        assert "effectTitle" in climate_effect
        assert "imageUrl" in climate_effect
        assert "isPossiblyLocal" in climate_effect

        assert type(climate_effect["effectDescription"]) == str
        assert type(climate_effect["effectId"]) == str
        assert type(climate_effect["effectScore"]) == float
        assert type(climate_effect["effectShortDescription"]) == str
        assert type(climate_effect["effectSolutions"]) == list
        assert type(climate_effect["effectSources"]) == list
        assert type(climate_effect["effectSpecificMythIRIs"]) == list
        assert type(climate_effect["effectTitle"]) == str
        assert type(climate_effect["imageUrl"]) == str
        assert type(climate_effect["isPossiblyLocal"]) == int

        assert len(climate_effect["effectSolutions"]) > 0
        for effect_solution in climate_effect["effectSolutions"]:
            assert "imageUrl" in effect_solution
            assert "iri" in effect_solution
            assert "longDescription" in effect_solution
            assert "shortDescription" in effect_solution
            assert "solutionSources" in effect_solution
            assert "solutionSpecificMythIRIs" in effect_solution
            assert "solutionTitle" in effect_solution
            assert "solutionType" in effect_solution

            assert is_none_or_type(effect_solution["imageUrl"], str)
            assert type(effect_solution["iri"]) == str
            assert type(effect_solution["longDescription"]) == str
            assert type(effect_solution["shortDescription"]) == str
            assert type(effect_solution["solutionSources"]) == list
            assert type(effect_solution["solutionSpecificMythIRIs"]) == list
            assert type(effect_solution["solutionTitle"]) == str
            assert type(effect_solution["solutionType"]) == str

        assert len(climate_effect["effectSources"]) > 0
        for effect_source in climate_effect["effectSources"]:
            assert type(effect_source) == str
