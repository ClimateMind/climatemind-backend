from app.errors.errors import InvalidUsageError
from enum import Enum
import uuid


class uuidType(Enum):
    """
    UUID types used to print for error responses
    """

    SESSION = 1
    QUIZ = 2
    USER = 3


def validate_uuid(uuid_to_validate, uuid_type):
    """
    UUIDs are required throughout the app for various purposes. SessionID for example
    is required for a user to access any page. We need to make sure UUIDs exist and
    are converted into proper UUID format when provided as strings.

    Parameters
    ==========
    uuid_to_validate: UUID as (str)
    uuid_type: Enum for type of UUID
    """
    if not uuid_to_validate:
        raise InvalidUsageError(message=f"{uuid_type.name}_UUID is required.")

    try:
        valid_uuid = uuid.UUID(uuid_to_validate)
    except ValueError:
        raise InvalidUsageError(
            message=f"{uuid_type.name}_UUID is improperly formatted."
        )

    return valid_uuid
