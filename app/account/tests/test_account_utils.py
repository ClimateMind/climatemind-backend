import typing

import pytest

from app.account.utils import is_email_valid, check_password_reset_link_is_valid
from app.errors.errors import (
    InvalidUsageError,
    UnauthorizedError,
    NotInDatabaseError,
)
from app.factories import faker, PasswordResetLinkFactory


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


@pytest.mark.parametrize(
    "uuid_to_test, error",
    (
        (None, InvalidUsageError),
        ("invalid uuid", InvalidUsageError),
        (faker.uuid4(), NotInDatabaseError),
    ),
)
def test_failed_check_password_reset_expiration(
    uuid_to_test: typing.Optional[str], error
):
    with pytest.raises(error):
        check_password_reset_link_is_valid(uuid_to_test)


def test_check_password_reset_link_is_valid():
    password_reset_uuid = PasswordResetLinkFactory().uuid
    assert check_password_reset_link_is_valid(password_reset_uuid)
