import pytest

from app.personal_values.enums import PersonalValue, DEFAULT_SEPARATOR


def test_personal_values_sorting():
    real_order_ids = list(PersonalValue)
    sorted_order_ids = sorted(PersonalValue)
    assert real_order_ids != sorted_order_ids, "Sorting by values (IDs) is wrong."

    keys_order = [v.key for v in PersonalValue]
    sorted_keys_order = sorted([v.key for v in PersonalValue])
    assert keys_order == sorted_keys_order, "Enum should by sorted by key"

    assert sorted_keys_order == PersonalValue.get_all_keys(), "Helper method order"


def test_personal_value_separation():
    pv_with_separator = PersonalValue.SELF_DIRECTION
    assert pv_with_separator.key == pv_with_separator.separated_key(
        DEFAULT_SEPARATOR
    ), "Default separation is underscore"

    dashed_key = pv_with_separator.key.replace("_", "-")
    assert dashed_key == pv_with_separator.separated_key(
        "-"
    ), "Default separation should be replaced with dash by method"
    assert (
        dashed_key == pv_with_separator.dashed_key
    ), "Default separation should be replaced with dash by property"

    spaced_key = pv_with_separator.key.replace("_", " ")
    assert spaced_key == pv_with_separator.separated_key(
        sep=" "
    ), "Default separation should be replaced with dash"

    pv_without_separator = PersonalValue.ACHIEVEMENT
    assert pv_without_separator.key == pv_without_separator.separated_key(
        "*&^%"
    ), "Should not affect PersonalValue without separator"


@pytest.mark.parametrize(
    "key, expected_representation",
    [
        ("self_direction", "Self Direction"),
        ("achievement", "Achievement"),
    ],
)
def test_personal_value_key_to_representation(key, expected_representation):
    assert PersonalValue[key].representation == expected_representation
