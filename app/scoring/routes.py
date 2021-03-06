from flask import jsonify, request, make_response


import uuid
import os

from app.scoring import bp
from app.scoring.persist_scores import persist_scores
from app.scoring.process_scores import ProcessScores

from app.scoring.store_ip_address import store_ip_address
from app.post_code.store_post_code import store_post_code, check_post_code
from app.errors.errors import InvalidUsageError, DatabaseError
from flask_cors import cross_origin

from app import auto

value_id_map = {
    1: "conformity",
    2: "tradition",
    3: "benevolence",
    4: "universalism",
    5: "self-direction",
    6: "stimulation",
    7: "hedonism",
    8: "achievement",
    9: "power",
    10: "security",
}


@bp.route("/scores", methods=["POST"])
@cross_origin()
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

    A session ID is saved with the scores in the database.

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
            message="Cannot post scores. Invalid number of questions provided"
        )

    process_scores = ProcessScores(questions)
    process_scores.calculate_scores("SetOne")

    if "SetTwo" in questions:
        process_scores.calculate_scores("SetTwo")
    process_scores.center_scores()
    value_scores = process_scores.get_value_scores()

    session_uuid = uuid.uuid4()
    value_scores["session-id"] = session_uuid
    persist_scores(value_scores)

    postal_code = parameter["zipCode"]

    if postal_code and check_post_code(postal_code):
        try:
            store_post_code(postal_code, session_uuid)
        except:
            raise DatabaseError(
                message="An error occurred while adding the postcode associated with these scores to the database."
            )

    process_scores.process_ip_address(request, session_uuid)

    response = {"sessionId": session_uuid}
    return jsonify(response), 201
