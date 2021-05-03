from flask import request

from app.post_code import bp
from app.post_code.store_post_code import store_post_code, check_post_code
from app.errors.errors import InvalidUsageError

from app import auto
import uuid


@bp.route("/post-code", methods=["POST"])
@auto.doc()
def post_code():
    """

    Accepts a sessionId and postCode and updates the Sessions object in the database
    to include the post code.

    """

    try:
        request_body = request.json
        session_uuid = uuid.UUID(request_body["sessionId"])
        post_code = request_body["postCode"]
    except:
        raise InvalidUsageError(
            message="Unable to post postcode. Check the request parameters."
        )

    if check_post_code(post_code):
        return store_post_code(post_code, session_uuid)
    else:
        raise InvalidUsageError(message="The postcode provided is not valid.")
