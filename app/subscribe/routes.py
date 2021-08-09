from flask import request

from app.subscribe import bp

from app.subscribe.store_subscription_data import store_subscription_data, check_email
from app.errors.errors import InvalidUsageError
from flask_cors import cross_origin
from flask import request

from app import auto

import uuid


@bp.route("/subscribe", methods=["POST"])
@cross_origin()
@auto.doc()
def subscribe():
    try:
        request_body = request.json
        email = request_body["email"]
        session_uuid = request.headers.get("X-Session-Id")
    except:
        raise InvalidUsageError(
            message="Unable to post subscriber information. Check the request parameters."
        )

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
