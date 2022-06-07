import re

from app.common.uuid import check_uuid_in_db, uuidType, validate_uuid
from app.errors.errors import (
    InvalidUsageError,
    UnauthorizedError,
    ExpiredError,
    ConflictError,
)


def is_email_valid(email: str) -> bool:
    """
    Checks an email format against the RFC 5322 specification.
    FIXME: could be replaced with marshmallow validator
     https://marshmallow.readthedocs.io/en/2.x-line/api_reference.html?highlight=Email#marshmallow.validate.Email
    """
    if not email:
        raise InvalidUsageError(
            message="Email and password must be included in the request body"
        )

    if not isinstance(email, str):
        raise UnauthorizedError(message="Wrong email or password. Try again.")

    # RFC 5322 Specification as Regex
    regex = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"
    (?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])
    *\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:
    (?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1
    [0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a
    \x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

    match = re.search(regex, email)
    return bool(match)


def check_password_reset_link_is_valid(password_reset_link_uuid):
    password_reset_link_uuid = validate_uuid(
        password_reset_link_uuid, uuidType.RESET_PASSWORD_LINK
    )
    reset_password = check_uuid_in_db(
        password_reset_link_uuid, uuidType.RESET_PASSWORD_LINK
    )
    if reset_password.expired:
        raise ExpiredError(message="Reset link is expired.")
    if reset_password.used:
        raise ConflictError(message="Reset link is used already.")
    return reset_password
