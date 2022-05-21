import pytest

from app.common.math_utils import as_percent


@pytest.mark.parametrize(
    "number, expected_percent",
    [
        (0.5, 50),
        (0.99, 99),
        (1, 100),
        # unexpected values don't raise an error
        (-0.5, -50),
        (10, 1000),
    ],
)
def test_as_percent(number, expected_percent):
    assert as_percent(number) == expected_percent
