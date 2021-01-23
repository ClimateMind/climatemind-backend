from flask import jsonify, request

import uuid
import os

from app.scoring import bp
from app.scoring.persist_scores import persist_scores

from app.scoring.store_ip_address import store_ip_address
from app.scoring.add_zip_code import add_zip_code

from app import auto

@bp.route("/scores", methods=["POST"])
@auto.doc()
def user_scores():
    """Users want to be able to get their score results after submitting
    the survey. This method checks for a POST request from the front-end
    containing a JSON object with the users scores.
    The user can answer 10 or 20 questions. If they answer 20, the scores
    are averaged between the 10 additional and 10 original questions to get
    10 corresponding value scores.
    Then to get a centered score for each value, each score value is subtracted
    from the overall average of all 10 or 20 questions. This is returned to the
    front-end.
    """
    try:
        parameter = request.json
    # todo: handle exceptions properly here
    except:
        return {"error": "Invalid user response"}, 400

    value_scores = {}
    overall_sum = 0
    num_of_responses = 10

    NUMBER_OF_SETS = 2
    POSITIVITY_CONSTANT = 3.5
    RESPONSES_TO_ADD = 10

    session_id = str(uuid.uuid4())

    questions = parameter["questionResponses"]
    zipcode = parameter["zipCode"]

    if len(questions["SetOne"]) < RESPONSES_TO_ADD:
        return {"error": "Not enough set one scores"}, 400
    elif len(questions["SetOne"]) > RESPONSES_TO_ADD:
        return {"error": "Too many set one scores"}, 400
        
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

    for value in questions["SetOne"]:
        questionID = value["questionId"]
        score = value["answerId"]
        overall_sum += score

        if value_id_map[questionID] in value_scores:
            return {"error": "Duplicate question ID"}, 400

        value_scores[value_id_map[questionID]] = score

    if "SetTwo" in questions:
        num_of_responses += RESPONSES_TO_ADD
        for value in questions["SetTwo"]:
            questionID = value["questionId"]
            score = value["answerId"]
            name = value_id_map[questionID]
            avg_score = (value_scores[name] + score) / NUMBER_OF_SETS
            overall_sum += score

            if questionID in value_scores.keys:
                return {"error": "Duplicate question ID"}, 400

            value_scores[name] = avg_score

    overall_avg = overall_sum / num_of_responses

    for value, score in value_scores.items():
        centered_score = (
            score - overall_avg + POSITIVITY_CONSTANT
        )  # To make non-negative

        value_scores[value] = centered_score

    value_scores["session-id"] = session_id

    try:
        persist_scores(value_scores)
    except KeyError:
        return {"error": "Invalid key"}, 400

    if zipcode:
        try:
            add_zip_code(zipcode, session_id)
        except:
            return {"error": "Error adding zipcode to db"}, 500

    if (
        os.environ["DATABASE_PARAMS"]
        == "Driver={ODBC Driver 17 for SQL Server};Server=tcp:db,1433;Database=sqldb-web-prod-001;Uid=sa;Pwd=Cl1mat3m1nd!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;"
    ):
        try:
            ip_address = None
            store_ip_address(ip_address, session_id)
        except:
            return {"error": "Error adding ip address locally"}, 500
    else:
        try:
            unprocessed_ip_address = request.headers.getlist("X-Forwarded-For")
            if len(unprocessed_ip_address) != 0:
                ip_address = unprocessed_ip_address[0]
            # request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
            else:
                ip_address = None
            store_ip_address(ip_address, session_id)
        except:
            return {"error": "Error adding ip address in cloud"}, 500

    response = {"sessionId": session_id}

    response = jsonify(response)
    return response, 201