from flask import request

from app.subscribe import bp

from app.subscribe.store_subscription_data import store_subscription_data

from app import auto

import uuid


@bp.route("/subscribe", methods=["POST"])
@auto.doc()
def subscribe():
    try:
        request_body = request.json
        email = request_body["email"]
        session_uuid = uuid.UUID(request_body["sessionId"])
        response = store_subscription_data(session_uuid, email)
        return response
    except:
        return {"error": "Invalid request"}, 400
