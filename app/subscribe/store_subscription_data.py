from app import db
from app.models import Signup, Sessions
from app.errors.errors import AlreadyExistsError, DatabaseError
import datetime
from datetime import timezone
import re
from app.errors.errors import InvalidUsageError, UnauthorizedError


def store_subscription_data(session_uuid, email):

    email_in_db = Signup.query.filter_by(email=email).first()
    valid_session_uuid = Sessions.query.get(session_uuid)

    if email_in_db:
        raise AlreadyExistsError(message="Subscriber email address")
    elif not valid_session_uuid:
        raise DatabaseError(
            message="Cannot save subscription information. Session id not in the database."
        )
    else:
        try:
            new_subscription = Signup()
            new_subscription.email = email
            new_subscription.session_uuid = session_uuid
            now = datetime.datetime.now(timezone.utc)
            new_subscription.signup_timestamp = now

            db.session.add(new_subscription)
            db.session.commit()

            response = {
                "message": "Successfully added email",
                "email": email,
                "sessionId": session_uuid,
                "datetime": now,
            }

            return response, 201
        except:
            raise DatabaseError(
                message="An error occurred while saving the subscription information to the database."
            )


def check_email(email):
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

    if re.search(regex, email):
        return True
    return False
