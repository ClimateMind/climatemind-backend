import pytest

from app.alignment.utils import (
    get_dashed_personal_values_names_from_vector,
    build_alignment_scores_response,
    as_percent,
)
from app.errors.errors import NotInDatabaseError
from app.factories import UserBJourneyFactory, faker
from app.personal_values.enums import PersonalValue


@pytest.mark.parametrize(
    "vector, expected_result",
    [
        ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0), []),
        ((1, 0, 0, 0, 0, 0, 0, 0, 0, 0), [PersonalValue.ACHIEVEMENT.dashed_key]),
        ((0, 0, 0, 0, 0, 0, 0, 0, 0, 1), [PersonalValue.UNIVERSALISM.dashed_key]),
        ((0, 0, 0, 0, 0, 0, 1, 0, 0, 0), [PersonalValue.SELF_DIRECTION.dashed_key]),
        (
            (1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
            PersonalValue.get_all_keys(sep="-"),
        ),
        (
            (1, 0, 0, 0, 0, 0, 0, 0, 0, 1),
            [
                PersonalValue.ACHIEVEMENT.dashed_key,
                PersonalValue.UNIVERSALISM.dashed_key,
            ],
        ),
    ],
)
def test_get_dashed_personal_values_names_from_vector(vector, expected_result):
    result = get_dashed_personal_values_names_from_vector(vector)
    assert result == expected_result


def test_build_alignment_scores_response():
    user_b_journey = UserBJourneyFactory()
    alignment_scores = user_b_journey.alignment_scores
    conversation = user_b_journey.conversation
    user_a = conversation.sender_user

    expected_response = {
        "overallSimilarityScore": as_percent(alignment_scores.overall_similarity_score),
        "topMatchPercent": alignment_scores.top_match_percent,
        "topMatchValue": alignment_scores.top_match_value,
        "userAName": user_a.first_name,
        "userBName": conversation.receiver_name,
    }
    response = build_alignment_scores_response(alignment_scores.alignment_scores_uuid)
    response_value_alignment = response.pop("valueAlignment")
    assert response == expected_response, "Response mirror DB object as expected"

    last_score = 100
    keys_in_response = []
    for value_alignment_from_response in response_value_alignment:
        current_score = value_alignment_from_response["score"]
        assert last_score >= current_score, "Array is not sorted"
        last_score = current_score

        keys_in_response.append(value_alignment_from_response["id"])

    assert set(keys_in_response) == set(
        PersonalValue.get_all_keys()
    ), "Keys from response are unique"
