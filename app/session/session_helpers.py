import os
from app import db
from app.models import Sessions
from app.errors.errors import DatabaseError


def store_session(session_uuid, session_created_timestamp, user_uuid):
    try:
        current_user_session = Sessions()
        current_user_session.session_uuid = session_uuid
        current_user_session.session_created_timestamp = session_created_timestamp
        if user_uuid:
            current_user_session.user_uuid = user_uuid

        db.session.add(current_user_session)
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while saving the session to the database."
        )


def process_ip_address(request, session_uuid):
    """
    Save a user's IP address information into the database with their session_uuid.
    Provided credentials are for the locally generated database (not production).

    Args:
        request: request
        session_uuid: UUID4

    Returns: Error and Status Code if they exist, otherwise None
    """
    if (
        os.environ["DATABASE_PARAMS"]
        == "Driver={ODBC Driver 17 for SQL Server};Server=tcp:db,1433;Database=sqldb-web-prod-001;Uid=sa;Pwd=Cl1mat3m1nd!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;"
    ):
        try:
            ip_address = None
            store_ip_address(ip_address, session_uuid)
        except:
            raise DatabaseError(
                message="An error occurred while saving the user's IP address to the local database."
            )
    else:
        try:
            unprocessed_ip_address = request.headers.getlist("X-Forwarded-For")
            if len(unprocessed_ip_address) != 0:
                ip_address = unprocessed_ip_address[0]
            else:
                ip_address = None
            store_ip_address(ip_address, session_uuid)
        except:
            raise DatabaseError(
                message="An error occurred while saving the user's IP address to the production database."
            )


def store_ip_address(ip_address, session_uuid):
    current_user_session = Sessions.query.filter_by(session_uuid=session_uuid).first()

    if ip_address:
        ip_address = str(ip_address)

    try:
        current_user_session.ip_address = ip_address
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while saving the IP address to the db."
        )

    return None
