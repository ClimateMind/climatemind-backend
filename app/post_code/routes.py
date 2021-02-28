from flask import request

from app.post_code import bp
from app.post_code.store_post_code import store_post_code

from app import auto


@bp.route("/post-code", methods=["POST"])
@auto.doc()
def post_code():
    """

    Accepts a sessionId and postCode and updates the Sessions object in the database
    to include the post code.

    """

    try:
        request_body = request.json
        session_uuid = request_body["sessionId"]
        postal_code = request_body["postCode"]
        return store_post_code(postal_code, session_uuid)

    except:
        return {"error": "Invalid request"}, 400
