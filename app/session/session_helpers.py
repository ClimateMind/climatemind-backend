import typing
import uuid
from datetime import datetime

from werkzeug.local import LocalProxy

from app import db
from app.common.local import check_if_local
from app.common.uuid import validate_uuid, uuidType, check_uuid_in_db
from app.errors.errors import DatabaseError
from app.models import Sessions

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


def store_session(
    session_uuid: uuid.UUID,
    session_created_timestamp: datetime,
    user_uuid: typing.Optional[uuid.UUID],
    ip_address: typing.Optional[str],
) -> None:  # raises DatabaseError
    """
    Stores the current session's id and timestamp in the sessions table.
    Checks if the user is logged in, and stores the user_uuid in the sessions table if they are.

    Args:
        session_uuid: UUID4
        session_created_timestamp: datetime
        user_uuid: UUID4
        ip_address: str

    Returns:
        None or DatabaseError
    """
    current_user_session = Sessions()
    current_user_session.session_uuid = session_uuid
    current_user_session.session_created_timestamp = session_created_timestamp
    current_user_session.ip_address = ip_address

    if user_uuid:
        current_user_session.user_uuid = user_uuid

    try:
        db.session.add(current_user_session)
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while saving the session to the database."
        )


def get_ip_address(request: LocalProxy) -> typing.Optional[str]:
    """
    Check's the user's IP address information.
    Provided credentials are for the locally generated database (not production).

    Args:
        request: request

    Returns: Error and Status Code if they exist, otherwise None
    """
    if check_if_local():
        ip_address = None
    else:
        unprocessed_ip_address = request.headers.getlist("X-Forwarded-For")
        if len(unprocessed_ip_address) != 0:
            ip_address = unprocessed_ip_address[0]
        else:
            ip_address = None

    return ip_address


def maybe_assign_session(request):
    """
    Assign a session to a user if not yet assigned.

    Args:
        request: the flask request

    Returns:
        None or DatabaseError
    """

    if (
        "Authorization" in request.headers
        and "X-Session-Id" in request.headers
        and request.headers["Authorization"] != ""
    ):
        verify_jwt_in_request()
        user_uuid = get_jwt_identity()

        session_uuid = request.headers.get("X-Session-Id")
        session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
        check_uuid_in_db(session_uuid, uuidType.SESSION)

        session = Sessions.query.filter_by(session_uuid=session_uuid).first()
        if session.user_uuid != user_uuid:
            session.user_uuid = user_uuid
            try:
                db.session.commit()
            except:
                raise DatabaseError(message="Could not assign the session to the user.")
