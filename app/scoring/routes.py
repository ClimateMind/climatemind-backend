from app.common.uuid import validate_uuid, uuidType, check_uuid_in_db
from flask import jsonify, request

import uuid

from app.scoring import bp
from app.scoring.process_scores import ProcessScores

from app.errors.errors import InvalidUsageError
from flask_cors import cross_origin

from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

from app import auto


@bp.route("/scores", methods=["POST"])
@cross_origin()
@jwt_required(optional=True)
@auto.doc()
def user_scores():
    """
    User scores are used to determine which solutions are best to serve
    the user. Users also want to be able to see their score results after
    submitting the survey.

    This route checks for a POST request from the front-end
    containing a JSON object with the users scores.

    The user can answer 10 or 20 questions. If they answer 20, the scores
    are averaged between the 10 additional and 10 original questions to get
    10 corresponding value scores.

    Then to get a centered score for each value, each score value is subtracted
    from the overall average of all 10 or 20 questions.

    A quiz ID is saved with the scores in the database.

    If authentication is provided and isUserB is not true, then the new calculated score is used to update the user's account's personal values.

    Returns: SessionID (UUID4)
    """

    parameter = request.json

    if not parameter:
        raise InvalidUsageError(
            message="Cannot post scores. No user response provided."
        )

    responses_to_add = 10

    questions = parameter["questionResponses"]

    if len(questions["SetOne"]) != responses_to_add:
        raise InvalidUsageError(
            message="Cannot post scores. Invalid number of questions provided."
        )

    process_scores = ProcessScores(questions)
    process_scores.calculate_scores("SetOne")

    if "SetTwo" in questions:
        process_scores.calculate_scores("SetTwo")
    process_scores.center_scores()
    value_scores = process_scores.get_value_scores()

    quiz_uuid = uuid.uuid4()
    value_scores["quiz_uuid"] = quiz_uuid

    session_uuid = request.headers.get("X-Session-Id")

    if not session_uuid:
        raise InvalidUsageError(message="Cannot post scores without a session ID.")

    validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    user_uuid = None
    if current_user:
        if not "isUserB" in parameter:
            user_uuid = current_user.user_uuid

    process_scores.persist_scores(user_uuid, session_uuid)

    response = {"quizId": quiz_uuid}
    return jsonify(response), 201
