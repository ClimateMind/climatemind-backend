from flask import request

from app.post_code import bp
from app.post_code.store_post_code import store_post_code, check_post_code
from app.auth.utils import check_uuid_in_db, uuidType, validate_uuid
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

    r = request.get_json(force=True, silent=True)

    if not r:
        raise InvalidUsageError(message="JSON body must be included.")

    quiz_uuid = r.get("quizId", None)
    quiz_uuid = validate_uuid(quiz_uuid, uuidType.QUIZ)
    check_uuid_in_db(quiz_uuid, uuidType.QUIZ)

    post_code = r.get("postCode", None)

    if not post_code:
        raise InvalidUsageError(
            message="Unable to post postcode. Check the request parameters."
        )

    if check_post_code(post_code):
        return store_post_code(post_code, quiz_uuid)
    else:
        raise InvalidUsageError(message="The postcode provided is not valid.")
