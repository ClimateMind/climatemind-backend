import typing
import uuid
from enum import Enum

from app import db
from app.errors.errors import InvalidUsageError, NotInDatabaseError
from app.models import (
    Sessions,
    Scores,
    Users,
    Conversations,
    AlignmentScores,
    PasswordResetLink,
)


class uuidType(Enum):
    """
    UUID types used to print for error responses
    """

    SESSION = 1
    QUIZ = 2
    USER = 3
    CONVERSATION = 4
    ALIGNMENT_SCORES = 5
    RESET_PASSWORD_LINK = 6


def validate_uuid(
    uuid_to_validate: typing.Union[uuid.UUID, str], uuid_type: uuidType
) -> uuid.UUID:
    """
    # FIXME: replace usage with marshmallow field
    #     uuid_field = fields.UUID()
    #     result = uuid_field.deserialize(value_to_validate)
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
) -> db.Model:  # raises NotInDatabaseError
    """
    FIXME: controversial solution with enum and conditions could be omitted
     if all primary keys have the same name like `uuid`
    A helper function to validate whether a UUID exists within our db.
    """
    object_from_db = None

    if uuid_type == uuidType.SESSION:
        object_from_db = Sessions.query.filter_by(session_uuid=uuid_to_validate).first()
    elif uuid_type == uuidType.QUIZ:
        object_from_db = Scores.query.filter_by(quiz_uuid=uuid_to_validate).first()
    elif uuid_type == uuidType.USER:
        object_from_db = Users.query.filter_by(user_uuid=uuid_to_validate).first()
    elif uuid_type == uuidType.CONVERSATION:
        object_from_db = Conversations.query.filter_by(
            conversation_uuid=uuid_to_validate,
            is_hidden=False,
        ).first()
    elif uuid_type == uuidType.ALIGNMENT_SCORES:
        object_from_db = AlignmentScores.query.filter_by(
            alignment_scores_uuid=uuid_to_validate
        ).first()
    elif uuid_type == uuidType.RESET_PASSWORD_LINK:
        object_from_db = PasswordResetLink.query.filter_by(
            uuid=uuid_to_validate
        ).first()

    if object_from_db:
        return object_from_db
    else:
        raise NotInDatabaseError(message=f"{uuid_type.name}_UUID is not in the db.")
