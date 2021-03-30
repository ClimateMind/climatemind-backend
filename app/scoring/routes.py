from flask import jsonify, request, abort

import uuid
import os

from app.scoring import bp
from app.scoring.persist_scores import persist_scores

from app.scoring.store_ip_address import store_ip_address
from app.post_code.store_post_code import store_post_code

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
        abort(400, description="No user response provided")

    responses_to_add = 10

    questions = parameter["questionResponses"]

    if len(questions["SetOne"]) != responses_to_add:
        abort(400, description="Invalid number of questions provided")

    value_scores, overall_avg = calculate_scores(questions)
    value_scores = center_scores(value_scores, overall_avg)

    session_uuid = uuid.uuid4()
    value_scores["session-id"] = session_uuid

    try:
        persist_scores(value_scores)
    except:
        abort(500, description="Unable to save provided question data")

    postal_code = parameter["zipCode"]

    if postal_code:
        try:
            store_post_code(postal_code, session_uuid)
        except:
            abort(500, description="Error adding zipcode to db")

    process_ip_address(request, session_uuid)

    response = {"sessionId": session_uuid}
    return jsonify(response), 201


def calculate_scores(
    questions, num_of_sets=2, num_of_responses=10, responses_to_add=10
):
    """
    Creates a dictionary of personal values and scores based on the user's responses.

    Args:
        questions: JSON data with questions, IDs and self-evaluated scores
        num_of_sets: Number of 10 question sets (Int)
        num_of_responses: How many questions the user answered (Int)
        responses_to_add: How many responses should be calculated (Int)

    Returns: value_scores - A dictionary of personal values and scores
             overall_avg - overall_sum / num_of_responses

    """
    overall_sum = 0
    value_scores = {}

    for value in questions["SetOne"]:
        question_id = value["questionId"]
        name = value_id_map[question_id]
        score = value["answerId"]
        overall_sum += score

        if value_id_map[question_id] in value_scores:
            abort(400, description="Duplicate question ID")
        value_scores[name] = score

    if "SetTwo" in questions:
        if len(questions["SetTwo"]) != responses_to_add:
            abort(400, description="Invalid number of questions provided")

        num_of_responses += responses_to_add
        for value in questions["SetTwo"]:
            question_id = value["questionId"]
            score = value["answerId"]
            name = value_id_map[question_id]
            avg_score = (value_scores[name] + score) / num_of_sets
            overall_sum += score

            if question_id in value_scores.keys():
                abort(400, description="Duplicate question ID")

            value_scores[name] = avg_score

    overall_avg = overall_sum / num_of_responses

    return value_scores, overall_avg


def center_scores(value_scores, overall_avg, positivity_constant=3.5):
    """
    User scores need to be non-negative and balanced based on their overall average score.

    Args:
        value_scores: A dictionary of personal values (str) and their scores (int)
        overall_avg: overall_sum (Int) / num_of_responses (Int)
        positivity_constant: Int

    Returns: value_scores

    """
    for value, score in value_scores.items():
        centered_score = score - overall_avg + positivity_constant

        value_scores[value] = centered_score
        return value_scores


def process_ip_address(request, session_uuid):
    """
    Save a user's IP address information into the database with their session_id.
    Provided credentials are for locally generated database (not production).

    Args:
        request: Request
        session_uuid: UUID4

    Returns: Error and Status Code if they exist, otherwise None
    """

    if (
        os.environ["DATABASE_PARAMS"]
        == "Driver={ODBC Driver 17 for SQL Server};Server=tcp:db,1433;Database=sqldb-web-prod-001;Uid=sa;Pwd=Cl1mat3m1nd!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;"
    ):
        try:
            ip_address = None
            store_ip_address(ip_address, session_uuid)
        except:
            abort(500, description="Error adding ip address locally")
    else:
        try:
            unprocessed_ip_address = request.headers.getlist("X-Forwarded-For")
            if len(unprocessed_ip_address) != 0:
                ip_address = unprocessed_ip_address[0]
            # request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
            else:
                ip_address = None
            store_ip_address(ip_address, session_uuid)
        except:
            abort(500, description="Error adding ip address in cloud")
