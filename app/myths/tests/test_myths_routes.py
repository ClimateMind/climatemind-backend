from flask import url_for
import pytest

from app.common.tests.test_utils import is_none_or_type


@pytest.mark.integration
def test_myths(client):
    response = client.get(url_for("myths.get_general_myths"))
    json = response.get_json()

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.access_control_allow_origin == "*"

    assert type(json) == dict
    assert "myths" in json
    assert type(json["myths"]) == list
    assert len(json["myths"]) != 0


@pytest.mark.integration
def test_myth_properties(client):
    response = client.get(url_for("myths.get_general_myths"))
    json = response.get_json()
    myths = json["myths"]

    assert len(myths) > 0
    for myth in myths:
        assert "faultyLogicDescription" in myth
        assert "iri" in myth
        assert "mythClaim" in myth
        assert "mythRebuttal" in myth
        assert "mythSources" in myth
        assert "mythTitle" in myth
        assert "mythVideos" in myth
        assert is_none_or_type(myth["faultyLogicDescription"], str)
        assert is_none_or_type(myth["iri"], str)
        assert is_none_or_type(myth["mythClaim"], str)
        assert is_none_or_type(myth["mythRebuttal"], str)
        assert is_none_or_type(myth["mythSources"], list)
        assert is_none_or_type(myth["mythTitle"], str)
        assert is_none_or_type(myth["mythVideos"], list)
