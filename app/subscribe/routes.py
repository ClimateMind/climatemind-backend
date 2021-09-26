from flask import request

from app.subscribe import bp

from app.subscribe.store_subscription_data import store_subscription_data, check_email
from app.errors.errors import InvalidUsageError
from app.auth.utils import uuidType, validate_uuid
from flask_cors import cross_origin
from flask import request

from app import auto

import uuid


@bp.route("/subscribe", methods=["POST"])
@cross_origin()
@auto.doc()
def subscribe():
    r = request.get_json(force=True, silent=True)

    if not r:
        raise InvalidUsageError(message="JSON body must be included.")

    email = r.get("email", None)
    session_uuid = r.get("sessionId", None)
    validate_uuid(session_uuid, uuidType.SESSION)

    if not session_uuid:
        raise InvalidUsageError(
            message="Cannot post subscriber information without a session ID."
        )

    if check_email(email):
        return store_subscription_data(session_uuid, email)
    else:
        raise InvalidUsageError(
            message="Cannot post subscriber information. Subscriber email is invalid."
        )
