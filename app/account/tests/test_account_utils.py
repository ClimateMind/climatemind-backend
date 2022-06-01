import pytest

from app.account.utils import is_email_valid
from app.errors.errors import InvalidUsageError, UnauthorizedError
from app.factories import faker


@pytest.mark.parametrize(
    "email,is_valid",
    (
        (faker.email(), True),
        (faker.email(), True),
        (faker.email(), True),
        ("a123@sdf.eu", True),
        ("123+sdf@SDF.EU", False),
        ("12.,$+213@SDF.EU", False),
        ("123SDF.EU", False),
        ("123SDFEU", False),
    ),
)
def test_is_email_valid(email: str, is_valid: bool):
    assert is_email_valid(email) == is_valid


@pytest.mark.parametrize(
    "email, error",
    (
        (None, InvalidUsageError),
        (1, UnauthorizedError),
    ),
)
def test_is_email_valid_with_error(email: str, error):
    with pytest.raises(error):
        is_email_valid(email)
