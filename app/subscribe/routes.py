from app.subscribe import bp

from app.subscribe.store_subscription_data import store_subscription_data
from app.email.utils import is_email_valid
from app.errors.errors import InvalidUsageError
from app.common.uuid import validate_uuid, uuidType, check_uuid_in_db
from flask_cors import cross_origin
from flask import request

from app import auto


@bp.route("/subscribe", methods=["POST"])
@cross_origin()
@auto.doc()
def subscribe():
    r = request.get_json(force=True, silent=True)

    if not r:
        raise InvalidUsageError(message="JSON body must be included.")

    email = r.get("email", None)
    session_uuid = r.get("sessionId", None)

    if not session_uuid:
        raise InvalidUsageError(
            message="Cannot post subscriber information without a session ID."
        )

    validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    if is_email_valid(email):
        return store_subscription_data(session_uuid, email)
    else:
        raise InvalidUsageError(
            message="Cannot post subscriber information. Subscriber email is invalid."
        )
