import typing
import uuid
from enum import Enum

from app.errors.errors import InvalidUsageError, NotInDatabaseError
from app.models import Sessions, Scores, Users, Conversations, AlignmentScores


class uuidType(Enum):
    """
    UUID types used to print for error responses
    """

    SESSION = 1
    QUIZ = 2
    USER = 3
    CONVERSATION = 4
    ALIGNMENT_SCORES = 5


def validate_uuid(
    uuid_to_validate: typing.Union[uuid.UUID, str], uuid_type: uuidType
) -> uuid.UUID:
    """
    UUIDs are required throughout the app for various purposes. SessionID for example
    is required for a user to access any page. We need to make sure UUIDs are provided,
    are converted into proper UUID format when provided as strings, and are valid.

    Parameters
    ==========
    uuid_to_validate: UUID as (str)
    uuid_type: Enum for type of UUID
    """
    if not uuid_to_validate:
        raise InvalidUsageError(message=f"{uuid_type.name}_UUID is required.")

    try:
        valid_uuid = uuid.UUID(uuid_to_validate)
    except (ValueError, TypeError, AttributeError):
        raise InvalidUsageError(
            message=f"{uuid_type.name}_UUID is improperly formatted."
        )

    return valid_uuid


def check_uuid_in_db(
    uuid_to_validate: typing.Union[uuid.UUID, str], uuid_type: uuidType
) -> None:  # raises NotInDatabaseError
    """
    A helper function to validate whether a UUID exists within our db.
    """
    uuid_exists_in_db = None

    if uuid_type == uuidType.SESSION:
        uuid_exists_in_db = Sessions.query.filter_by(
            session_uuid=uuid_to_validate
        ).first()
    elif uuid_type == uuidType.QUIZ:
        uuid_exists_in_db = Scores.query.filter_by(quiz_uuid=uuid_to_validate).first()
    elif uuid_type == uuidType.USER:
        uuid_exists_in_db = Users.query.filter_by(user_uuid=uuid_to_validate).first()
    elif uuid_type == uuidType.CONVERSATION:
        uuid_exists_in_db = Conversations.query.filter_by(
            conversation_uuid=uuid_to_validate
        ).first()
    elif uuid_type == uuidType.ALIGNMENT_SCORES:
        uuid_exists_in_db = AlignmentScores.query.filter_by(
            alignment_scores_uuid=uuid_to_validate
        ).first()

    if not uuid_exists_in_db:
        raise NotInDatabaseError(message=f"{uuid_type.name}_UUID is not in the db.")
