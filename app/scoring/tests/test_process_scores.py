import pytest

from app.scoring.process_scores import ProcessScores, get_scores_list, get_scores_map
from .data import process_scores_data
from app.factories import ScoresFactory
from app.personal_values.enums import PersonalValue


@pytest.mark.parametrize("questions", process_scores_data)
def test_process_scores(questions):
    process_scores = ProcessScores(questions)
    process_scores.calculate_scores("SetOne")

    if "SetTwo" in questions:
        process_scores.calculate_scores("SetTwo")
    process_scores.center_scores()
    value_scores = process_scores.get_value_scores()

    assert all(
        [v > 0 for v in value_scores.values()]
    ), "Should produce numerically positive scores"


def test_get_scores_list_sorted():
    score = ScoresFactory()
    res_scores_list = get_scores_list(score.quiz_uuid)
    assert len(res_scores_list) == len(PersonalValue), "Same length"

    sorted_personal_values = sorted(PersonalValue.get_all_keys())
    for pv_key, result_score_value in zip(sorted_personal_values, res_scores_list):
        assert getattr(score, pv_key) == result_score_value, "Ordering is wrong"


def test_get_scores_map():
    scores = ScoresFactory()
    scores_map = get_scores_map(scores)
    for personal_value_key in PersonalValue.get_all_keys():
        personal_value_score = scores_map.pop(personal_value_key)
        db_score_for_personal_value = getattr(scores, personal_value_key)
        assert db_score_for_personal_value == personal_value_score
    assert not scores_map, "Scores map should contain Personal Values only"
