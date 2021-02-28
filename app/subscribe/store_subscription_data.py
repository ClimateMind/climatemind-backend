from app import db
from app.models import Signup, Sessions
import datetime
from datetime import timezone
import re


def store_subscription_data(session_uuid, email):
    try:
        valid_email = check_email(email)
        in_db = Signup.query.filter_by(email=email).first()
        valid_session_uuid = Sessions.query.get(session_uuid)
        if in_db:
            return {"error": "Email already in db"}, 409
        elif not valid_session_uuid:
            return {"error": "Invalid session ID"}, 500
        elif valid_email:
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
                return {"error": "Error saving to db"}, 500
        else:
            return {"error": "Invalid email"}, 400
    except:
        return {"error": "Error querying the db"}, 500


def check_email(email):
    """
    Checks an email format against the RFC 5322 specification.
    """

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
