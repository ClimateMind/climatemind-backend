import pytest

from app.scoring.process_scores import ProcessScores
from .data import process_scores_data


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
