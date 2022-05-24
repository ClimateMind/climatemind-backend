import pytest

from app.scoring.process_alignment_scores import (
    get_rank_map,
    get_alignment_map,
    get_max,
)
from app.personal_values.enums import PersonalValue


def test_get_rank_map():
    data_map = {
        PersonalValue.ACHIEVEMENT.key: (0.9, 1),
        PersonalValue.SELF_DIRECTION.key: (0.8, 2),
        PersonalValue.SECURITY.key: (0.8, 2),
        PersonalValue.BENEVOLENCE.key: (0.6, 4),
        PersonalValue.UNIVERSALISM.key: (0.5, 5),
        PersonalValue.STIMULATION.key: (0.4, 6),
        PersonalValue.CONFORMITY.key: (0.3, 7),
        PersonalValue.POWER.key: (0.2, 8),
        PersonalValue.TRADITION.key: (0.2, 8),
        PersonalValue.HEDONISM.key: (0.0, 10),
    }
    score_map = {name: data[0] for (name, data) in data_map.items()}
    expected_rank_map = {name: data[1] for (name, data) in data_map.items()}
    actual_rank_map = get_rank_map(score_map)
    assert (
        actual_rank_map == expected_rank_map
    ), "Rank map does not have expected values."


def test_get_alignment_map():
    data_map = {
        PersonalValue.ACHIEVEMENT.key: (1, 5, 0.728),
        PersonalValue.SELF_DIRECTION.key: (2, 7, 0.563),
        PersonalValue.SECURITY.key: (2, 8, 0.434),
        PersonalValue.BENEVOLENCE.key: (4, 3, 0.853),
        PersonalValue.UNIVERSALISM.key: (5, 2, 0.769),
        PersonalValue.STIMULATION.key: (6, 5, 0.743),
        PersonalValue.CONFORMITY.key: (7, 3, 0.620),
        PersonalValue.POWER.key: (8, 10, 0.509),
        PersonalValue.TRADITION.key: (8, 9, 0.572),
        PersonalValue.HEDONISM.key: (10, 1, 0.000),
    }
    userA_rank_map = {name: data[0] for (name, data) in data_map.items()}
    userB_rank_map = {name: data[1] for (name, data) in data_map.items()}
    expected_alignment_map = {name: data[2] for (name, data) in data_map.items()}
    actual_raw_alignment_map = get_alignment_map(userA_rank_map, userB_rank_map)
    actual_alignment_map = {
        name: round(value, 3) for (name, value) in actual_raw_alignment_map.items()
    }
    assert (
        actual_alignment_map == expected_alignment_map
    ), "Alignment map does not have expected values."


def test_get_max():
    data_map = {
        PersonalValue.ACHIEVEMENT.key: 0.728,
        PersonalValue.SELF_DIRECTION.key: 0.563,
        PersonalValue.SECURITY.key: 0.434,
        PersonalValue.BENEVOLENCE.key: 0.853,
        PersonalValue.UNIVERSALISM.key: 0.769,
        PersonalValue.STIMULATION.key: 0.743,
        PersonalValue.CONFORMITY.key: 0.620,
        PersonalValue.POWER.key: 0.509,
        PersonalValue.TRADITION.key: 0.572,
        PersonalValue.HEDONISM.key: 0.000,
    }
    expected_max = (PersonalValue.BENEVOLENCE.key, 0.853)

    actual_max = get_max(data_map)
    assert actual_max == expected_max, "The correct max value was not chosen."
