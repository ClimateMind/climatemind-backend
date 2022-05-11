import pytest

from app.alignment.utils import get_dashed_personal_values_names_from_vector
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
