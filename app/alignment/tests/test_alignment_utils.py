import pytest

from app.alignment.utils import (
    get_dashed_personal_values_names_from_vector,
    build_alignment_scores_response,
    get_aligned_scores_alignments,
)
from app.common.math_utils import as_percent
from app.factories import UserBJourneyFactory, AlignmentScoresFactory
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

    top_match_value = alignment_scores.top_match_value
    top_match_value_representation = PersonalValue[top_match_value].representation
    expected_response = {
        "overallSimilarityScore": as_percent(alignment_scores.overall_similarity_score),
        "topMatchPercent": alignment_scores.top_match_percent,
        "topMatchValue": top_match_value_representation,
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


def test_get_aligned_scores_alignments():
    aligned_score = AlignmentScoresFactory()
    aligned_scores_map = {
        field.replace("_alignment", ""): score
        for field, score in aligned_score.__dict__.items()
        if field.endswith("_alignment")
    }
    expected_aligned_scores_alignments = []
    for key in sorted(aligned_scores_map):
        expected_aligned_scores_alignments.append(aligned_scores_map[key])

    aligned_scores_alignments = get_aligned_scores_alignments(aligned_score)
    assert (
        aligned_scores_alignments == expected_aligned_scores_alignments
    ), "All alignments should be returned in alphabetical order"
