import os
import uuid
from json import dumps, load

from flask import make_response, jsonify, request
from flask import request, Response, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from typing import Tuple

from knowledge_graph import app, db, auto
from knowledge_graph.models import Scores
from knowledge_graph.persist_scores import persist_scores

from knowledge_graph.score_nodes import (
    get_user_nodes,
    get_user_actions,
    get_user_general_myth_nodes,
    get_user_general_solution_nodes,
    get_specific_myth_info,
)

from knowledge_graph.store_ip_address import store_ip_address


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


@app.route("/", methods=["GET"])
@auto.doc()
def home() -> Tuple[str, int]:
    return "<h1>API for climatemind ontology</h1>", 200


@app.route("/ontology", methods=["GET"])
@auto.doc()
def query() -> Tuple[Response, int]:
    """
    description: Resource for accessing the contents of the ontology via queries.
    """
    searchQueries = request.args.getlist("query")

    searchResults = {}

    mind = app.config["MIND"]

    try:
        for keyword in searchQueries:
            searchResults[keyword] = mind.search(keyword)

    except ValueError:
        # todo: currently returns no results at all if 1 keyword in an array isn't found. fix this.
        return make_response("query keyword not found"), 400

    response = Response(dumps(searchResults))
    response.headers["Content-Type"] = "application/json"

    return response, 200


@app.route("/questions", methods=["GET"])
@auto.doc()
def get_questions() -> Tuple[Response, int]:
    """
    Returns the list of available questions that can be presented to
    the user.
    """
    try:
        file = os.path.join(os.getcwd(), "json_files", "schwartz_questions.json")
        with open(file) as json_file:
            data = load(json_file)
    except FileNotFoundError:
        return make_response("Schwartz Questions not Found"), 400

    response = Response(dumps(data))
    response.headers["Content-Type"] = "application/json"

    return response, 200


@app.route("/scores", methods=["POST"])
@auto.doc()
def user_scores() -> Tuple[Response, int]:
    """
    Users want to be able to get their score results after submitting the survey.
    The user can answer 10 or 20 questions. If they answer 20, the scores are averaged between the 10 additional and 10 original questions to get 10 corresponding value scores.
    Then to get a centered score for each value, each score value is subtracted from the overall average of all 10 or 20 questions. This score is returned in the response. on our server
    """
    if request.method == "POST":
        return receive_user_scores()


def receive_user_scores() -> Tuple[Response, int]:
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
    except Exception as ex:
        print(ex)
        return make_response("Invalid User Response"), 400

    value_scores = {}
    overall_sum = 0
    num_of_responses = 10

    NUMBER_OF_SETS = 2
    POSITIVITY_CONSTANT = 3.5
    RESPONSES_TO_ADD = 10

    session_id = str(uuid.uuid4())

    questions = parameter["questionResponses"]

    if len(questions["SetOne"]) < RESPONSES_TO_ADD:
        return make_response("not enough set one scores", 400)
    elif len(questions["SetOne"]) > RESPONSES_TO_ADD:
        return make_response("too many set one scores", 400)

    for value in questions["SetOne"]:
        questionID = value["questionId"]
        score = value["answerId"]
        overall_sum += score

        if value_id_map[questionID] in value_scores:
            return make_response("duplicate question ID", 400)

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
                return make_response("duplicate question ID", 400)

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
        return make_response("invalid key"), 400

    if (
        os.environ["DATABASE_PARAMS"]
        == "Driver={ODBC Driver 17 for SQL Server};Server=tcp:db,1433;Database=sqldb-web-prod-001;Uid=sa;Pwd=Cl1mat3m1nd!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;"
    ):
        try:
            ip_address = None
            store_ip_address(ip_address, session_id)
        except Exception:
            return make_response({"error": "error adding ip address locally"}), 500
    else:
        try:
            unprocessed_ip_address = request.headers.getlist("X-Forwarded-For")
            if len(unprocessed_ip_address) != 0:
                ip_address = unprocessed_ip_address[0]
            # request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
            else:
                ip_address = None
            store_ip_address(ip_address, session_id)
        except Exception:
            return make_response({"error": "error adding ip address in cloud"}), 500

    response = {"sessionId": session_id}

    response = jsonify(response)
    return response, 201


@app.route("/personal_values", methods=["GET"])
@auto.doc()
def get_personal_values():
    """
    Returns the top 3 personal values of a user given a session ID.
    """
    try:
        session_id = str(request.args.get("session-id"))
    # TODO: catch exceptions properly here
    except Exception:
        return make_response("Invalid Session ID Format or No ID Provided"), 400

    scores = Scores.query.filter_by(session_id=session_id).first()
    if scores:
        scores = scores.__dict__
        personal_values_categories = [
            "security",
            "conformity",
            "benevolence",
            "tradition",
            "universalism",
            "self_direction",
            "stimulation",
            "hedonism",
            "achievement",
            "power",
        ]
        sorted_scores = {key: scores[key] for key in personal_values_categories}
        # del scores["_sa_instance_state"]
        # del scores["session_id"]
        # del scores["user_id"]
        # del scores["scores_id"]

        top_scores = sorted(sorted_scores, key=sorted_scores.get, reverse=True)[:3]

        try:
            file = os.path.join(os.getcwd(), "json_files", "value_descriptions.json")
            with open(file) as f:
                value_descriptions = load(f)
        except FileNotFoundError:
            return make_response("Value Descriptions File Not Found"), 400
        descriptions = [value_descriptions[score] for score in top_scores]

        scores_and_descriptions = []
        for i in range(len(top_scores)):
            scores_and_descriptions.append(descriptions[i])
        response = {"personalValues": scores_and_descriptions}
        return jsonify(response), 200

    else:
        return make_response("Invalid Session ID - Internal Server Error"), 400


@app.route("/get_actions", methods=["GET"])
@auto.doc()
def get_actions():
    """
    The front-end needs to request personalized actions to take against climate change
    based on a specified climate effect.
    """
    effect_name = str(request.args.get("effect-name"))

    try:
        actions = get_user_actions(effect_name)
    except:
        return make_response("Invalid climate effect or no actions found"), 400

    response = jsonify({"actions": actions})
    return response, 200


@app.route("/feed", methods=["GET"])
@auto.doc()
def get_feed():
    """
    The front-end needs to request personalized climate change effects that are most
    relevant to a user to display in the user's feed.

    """
    N_FEED_CARDS = 5

    session_id = str(request.args.get("session-id"))
    try:
        scores = db.session.query(Scores).filter_by(session_id=session_id).first()
    # TODO: catch exceptions properly here
    except Exception:
        return make_response("Invalid Session ID or No Information for ID")

    scores = scores.__dict__
    del scores["_sa_instance_state"]

    recommended_nodes = get_user_nodes(scores, N_FEED_CARDS)
    feed_entries = {"climateEffects": recommended_nodes}
    return jsonify(feed_entries), 200


@app.route("/myths", methods=["GET"])
@auto.doc()
def get_general_myths():
    """
    The front-end needs general myths list and information to serve to user when they click the general myths menu button.
    General myths are ordered based on relevance predicted from users personal values.
    """
    # session_id = str(request.args.get("session-id"))
    # try:
    # scores = db.session.query(Scores).filter_by(session_id=session_id).first()
    # TODO: catch exceptions properly here
    # except Exception:
    #    return make_response("Invalid Session ID or No Information for ID")

    # scores = scores.__dict__
    # del scores["_sa_instance_state"]

    recommended_general_myths = get_user_general_myth_nodes()
    climate_general_myths = {"myths": recommended_general_myths}
    return jsonify(climate_general_myths), 200


@app.route("/myths/<string:iri>", methods=["GET"])
def get_myth_info(iri):
    myth_info = get_specific_myth_info(iri)

    if myth_info:
        specific_myth_info = {"myth": myth_info}
        return jsonify(specific_myth_info), 200
    else:
        return make_response({"error": "IRI does not exist"}), 400


@app.route("/solutions", methods=["GET"])
@auto.doc()
def get_general_solutions():
    """
    The front-end needs general myths list and information to serve to user when they click the general myths menu button.
    General myths are ordered based on relevance predicted from users personal values.
    """
    # session_id = str(request.args.get("session-id"))
    # try:
    # scores = db.session.query(Scores).filter_by(session_id=session_id).first()
    # TODO: catch exceptions properly here
    # except Exception:
    #    return make_response("Invalid Session ID or No Information for ID")

    # scores = scores.__dict__
    # del scores["_sa_instance_state"]

    recommended_general_solutions = get_user_general_solution_nodes()
    climate_general_solutions = {"solutions": recommended_general_solutions}
    return jsonify(climate_general_solutions), 200


@app.route("/documentation")
def documentation():
    return auto.html()
