from app import db
from app.models import Signup
from app.errors.errors import AlreadyExistsError, DatabaseError
import datetime
from datetime import timezone


def store_subscription_data(session_uuid, email):

    email_in_db = Signup.query.filter_by(signup_email=email).first()

    if email_in_db:
        raise AlreadyExistsError(message="Subscriber email address")
    else:
        try:
            new_subscription = Signup()
            new_subscription.signup_email = email
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
