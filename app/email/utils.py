import re

from app.errors.errors import InvalidUsageError, UnauthorizedError


def is_email_valid(email: str) -> bool:
    """
    Checks an email format against the RFC 5322 specification.
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
