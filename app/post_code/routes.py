from flask import request

from app.post_code import bp
from app.post_code.store_post_code import store_post_code, check_post_code
from app.errors.errors import InvalidUsageError
from flask_cors import cross_origin

from app import auto
import uuid


@bp.route("/post-code", methods=["POST"])
@cross_origin()
@auto.doc()
def post_code():
    """

    Accepts a quizId and postCode and updates the Scores object in the database
    to include the post code.

    """

    try:
        request_body = request.json
        quiz_uuid = uuid.UUID(request_body["quizId"])
        post_code = request_body["postCode"]
    except:
        raise InvalidUsageError(
            message="Unable to post postcode. Check the request parameters."
        )

    if check_post_code(post_code):
        return store_post_code(post_code, quiz_uuid)
    else:
        raise InvalidUsageError(message="The postcode provided is not valid.")
