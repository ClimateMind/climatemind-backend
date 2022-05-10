from app.models import AlignmentScores, Scores
from app.personal_values.enums import PersonalValue


def test_alignment_score_fields_equals_to_personal_values():
    alignment_fields = [
        k.replace("_alignment", "")
        for k in AlignmentScores.__dict__.keys()
        if k.endswith("_alignment")
    ]

    assert set(alignment_fields) == set(
        PersonalValue.get_all_keys()
    ), "All AlignmentScores _alignment fields should be equal to PersonalValues"


def test_personal_values_in_scores_fields():
    for v in PersonalValue:
        assert hasattr(Scores, v.key), f"{v.key} field is missing in Scores class"
