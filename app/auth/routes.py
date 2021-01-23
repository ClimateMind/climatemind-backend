from flask import request

from app.auth import bp

from app.auth.store_subscription_data import store_subscription_data

from app import auto


@bp.route("/subscribe", methods=["POST"])
@auto.doc()
def subscribe():
    try:
        request_body = request.json
        email = request_body["email"]
        session_id = request_body["sessionId"]
        response = store_subscription_data(session_id, email)
        return response
    except:
        return {"error": "Invalid request"}, 400
