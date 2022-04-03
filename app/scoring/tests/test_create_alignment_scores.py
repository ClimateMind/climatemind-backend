import pytest

import app.scoring.process_alignment_scores as pas

### Example data was taken from https://docs.google.com/document/d/1cqmBvNd8sWV1d6EvmTLgp6DlR3h1RVgW7pNDGgmV_k4/edit


def test_get_rank_map():
    data_map = {
        "achievement": (0.9, 1),
        "self_direction": (0.8, 2),
        "security": (0.8, 2),
        "benevolence": (0.6, 4),
        "universalism": (0.5, 5),
        "stimulation": (0.4, 6),
        "conformity": (0.3, 7),
        "power": (0.2, 8),
        "tradition": (0.2, 8),
        "hedonism": (0.0, 10),
    }
    score_map = {name: data[0] for (name, data) in data_map.items()}
    expected_rank_map = {name: data[1] for (name, data) in data_map.items()}
    actual_rank_map = pas.get_rank_map(score_map)
    assert (
        actual_rank_map == expected_rank_map
    ), "Rank map does not have expected values."


def test_get_alignment_map():
    data_map = {
        "achievement": (1, 5, 0.728),
        "self_direction": (2, 7, 0.563),
        "security": (2, 8, 0.434),
        "benevolence": (4, 3, 0.853),
        "universalism": (5, 2, 0.769),
        "stimulation": (6, 5, 0.743),
        "conformity": (7, 3, 0.620),
        "power": (8, 10, 0.509),
        "tradition": (8, 9, 0.572),
        "hedonism": (10, 1, 0.000),
    }
    userA_rank_map = {name: data[0] for (name, data) in data_map.items()}
    userB_rank_map = {name: data[1] for (name, data) in data_map.items()}
    expected_alignment_map = {name: data[2] for (name, data) in data_map.items()}
    actual_raw_alignment_map = pas.get_alignment_map(userA_rank_map, userB_rank_map)
    actual_alignment_map = {
        name: round(value, 3) for (name, value) in actual_raw_alignment_map.items()
    }
    assert (
        actual_alignment_map == expected_alignment_map
    ), "Alignment map does not have expected values."


def test_get_max():
    data_map = {
        "achievement": 0.728,
        "self_direction": 0.563,
        "security": 0.434,
        "benevolence": 0.853,
        "universalism": 0.769,
        "stimulation": 0.743,
        "conformity": 0.620,
        "power": 0.509,
        "tradition": 0.572,
        "hedonism": 0.000,
    }

    expected_max = ("benevolence", 0.853)
    actual_max = pas.get_max(data_map)
    assert actual_max == expected_max, "The correct max value was not chosen."
