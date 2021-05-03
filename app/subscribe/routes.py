from flask import request

from app.subscribe import bp

from app.subscribe.store_subscription_data import store_subscription_data, check_email
from app.errors.errors import InvalidUsageError

from app import auto

import uuid


@bp.route("/subscribe", methods=["POST"])
@auto.doc()
def subscribe():
    try:
        request_body = request.json
        email = request_body["email"]
        session_uuid = uuid.UUID(request_body["sessionId"])
    except:
        raise InvalidUsageError(
            message="Unable to post subscriber information. Check the request parameters."
        )

    if check_email(email):
        return store_subscription_data(session_uuid, email)
    else:
        raise InvalidUsageError(
            message="Cannot post subscriber information. Subscriber email is invalid."
        )
