import pytest
from flask import url_for

from app.factories import UserBJourneyFactory, SessionsFactory, faker


@pytest.mark.integration
def test_get_alignment(client):
    user_b_journey = UserBJourneyFactory()
    alignment_scores = user_b_journey.alignment_scores
    session = SessionsFactory()

    faked_uuid = faker.uuid4()
    error_response = client.get(
        url_for(
            "alignment.get_alignment",
            alignment_scores_uuid=faked_uuid,
        ),
        headers=[("X-Session-Id", session.session_uuid)],
    )
    assert error_response.status_code == 404

    response = client.get(
        url_for(
            "alignment.get_alignment",
            alignment_scores_uuid=alignment_scores.alignment_scores_uuid,
        ),
        headers=[("X-Session-Id", session.session_uuid)],
    )
    assert response.status_code == 200

    # The exact values are tested in UT
    expected_response_keys = {
        "overallSimilarityScore",
        "topMatchPercent",
        "topMatchValue",
        "valueAlignment",
        "userAName",
        "userBName",
    }
    assert (
        set(response.json.keys()) == expected_response_keys
    ), "Response contain all keys we need"
