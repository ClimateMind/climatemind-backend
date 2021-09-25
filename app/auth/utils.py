from app.models import Sessions, Scores, Users
from app.errors.errors import DatabaseError, InvalidUsageError
from enum import Enum
from flask import request
import uuid, os


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
    is required for a user to access any page. We need to make sure UUIDs are provided,
    are converted into proper UUID format when provided as strings, and are

    Parameters
    ==========
    uuid_to_validate: UUID as (str)
    uuid_type: Enum for type of UUID
    """
    if not uuid_to_validate:
        raise InvalidUsageError(message=f"{uuid_type.name}_UUID is required.")

    try:
        valid_uuid = uuid.UUID(uuid_to_validate)
    except (ValueError, TypeError):
        raise InvalidUsageError(
            message=f"{uuid_type.name}_UUID is improperly formatted."
        )

    return valid_uuid


def check_uuid_in_db(uuid_to_validate, uuid_type):
    """
    A helper function to validate whether a UUID exists within our db.
    """
    uuid_in_db = None

    if uuid_type.name == "SESSION":
        uuid_in_db = Sessions.query.filter_by(session_uuid=uuid_to_validate).first()
    elif uuid_type.name == "QUIZ":
        uuid_in_db = Scores.query.filter_by(quiz_uuid=uuid_to_validate).first()
    elif uuid_type.name == "USER":
        uuid_in_db = Users.query.filter_by(user_uuid=uuid_to_validate).first()

    if not uuid_in_db:
        raise DatabaseError(message=f"{uuid_type.name}_UUID is not in the db.")

    return uuid_in_db


def check_if_local():
    """
    A helper function to check whether a request is being made from a local connection or on the
    live website.
    """
    local = None

    if (
        os.environ["DATABASE_PARAMS"]
        == "Driver={ODBC Driver 17 for SQL Server};Server=tcp:db,1433;Database=sqldb-web-prod-001;Uid=sa;Pwd=Cl1mat3m1nd!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;"
    ):
        local = request.remote_addr == "127.0.0.1" or os.environ.get("VPN")

    return local
