from flask_swagger_ui import get_swaggerui_blueprint
from json import dumps, load, loads
from typing import Tuple

from flask import request, make_response, Response, send_from_directory, jsonify

from knowledge_graph import app, db
from knowledge_graph.persist_scores import persist_scores
from knowledge_graph.score_nodes import get_user_nodes
from knowledge_graph.models import Scores

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from collections import Counter

import uuid

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

# Swagger Stuff
SWAGGER_URL = "/swagger"
APP_URL = "/static/openapi.yaml"
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL, APP_URL, config={"app_name": "Climage Mind Backend"}
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route("/swagger/<path:path>")
def send_file(path):
    return send_from_directory("/swagger", path)


# End Swagger Stuff


spec = APISpec(
    title="ClimateMind API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


@app.route("/", methods=["GET"])
def home() -> Tuple[str, int]:
    return "<h1>API for climatemind ontology</h1>", 200


@app.route("/ontology", methods=["GET"])
def query() -> Tuple[Response, int]:
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
def get_questions() -> Tuple[Response, int]:
    try:
        with open("schwartz_questions.json") as json_file:
            data = load(json_file)
    except FileNotFoundError:
        return make_response("Schwartz Questions not Found"), 400

    response = Response(dumps(data))
    response.headers["Content-Type"] = "application/json"

    return response, 200


@app.route("/scores", methods=["POST"])
def user_scores() -> Tuple[Response, int]:
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
    except:
        return make_response("Invalid User Response"), 400

    value_scores = {}
    overall_sum = 0
    num_of_responses = 10

    NUMBER_OF_SETS = 2
    POSITIVITY_CONSTANT = 3.5
    RESPONSES_TO_ADD = 10

    session_id = uuid.uuid4()

    for value in parameter["SetOne"]:
        questionID = value["id"]
        score = value["score"]
        overall_sum += score
        value_scores[value_id_map[questionID]] = score

    if parameter["SetTwo"]:
        num_of_responses += RESPONSES_TO_ADD
        for value in parameter["SetTwo"]:
            questionID = value["id"]
            score = value["score"]
            name = value_id_map[questionID]
            avg_score = (value_scores[name] + score) / NUMBER_OF_SETS
            overall_sum += score
            value_scores[name] = avg_score

    overall_avg = overall_sum / num_of_responses

    for value, score in value_scores.items():
        centered_score = (
            score - overall_avg + POSITIVITY_CONSTANT
        )  # To make non-negative

        value_scores[value] = centered_score

    value_scores["session-id"] = str(session_id)

    persist_scores(value_scores)

    response = Response(dumps(value_scores))
    return response, 200


@app.route("/personal_values", methods=["GET"])
def get_personal_values():
    """Given a session-id, this returns the top three personal values for a user"""
    try:
        session_id = int(request.args.get("session-id"))
    except:
        return make_response("Invalid Session ID Format or No ID Provided"), 400

    scores = db.session.query(Scores).filter_by(session_id=session_id).first()
    if scores:
        scores = scores.__dict__
        del scores["_sa_instance_state"]

        top_scores = sorted(scores, key=scores.get, reverse=True)[:3]
        try:
            with open("value_descriptions.json", "r") as f:
                value_descriptions = load(f)
        except FileNotFoundError:
            return make_response("Value Descriptions File Not Found"), 400
        descriptions = [value_descriptions[score] for score in top_scores]

        scores_and_descriptions = []
        for i in range(len(top_scores)):
            d = {}
            d["valueName"] = top_scores[i]
            d["valueDesc"] = descriptions[i]
            scores_and_descriptions.append(d)
        return jsonify(scores_and_descriptions)

    else:
        return make_response("Invalid Session ID - Internal Server Error"), 400


@app.route("/get_actions", methods=["POST"])
def get_actions():
    """Temporary test function to take a JSON full of user scores and calculate the
    best nodes to return to a user. Will be deprecated and replaced by /feed.

    """
    try:
        scores = request.json
    except:
        return make_response("Invalid JSON"), 400
    recommended_nodes = get_user_nodes(scores)
    response = Response(dumps(recommended_nodes))
    return response, 200


with app.test_request_context():
    spec.path(view=get_actions)
    spec.path(view=get_personal_values)
    spec.path(view=user_scores)
    spec.path(view=get_questions)
    spec.path(view=query)


@app.route("/spec")
def get_apispec():
    return jsonify(spec.to_dict())


@app.route("/feed", methods=["POST"])
def get_feed():
    """The front-end needs to request personalized climate change effects that are most
    relevant to a user to display in the user's feed.

    """
    session_id = str(request.args.get("session-id"))
    try:
        scores = db.session.query(Scores).filter_by(session_id=session_id).first()
    except:
        return make_response("Invalid Session ID or No Information for ID")

    scores = scores.__dict__
    del scores["_sa_instance_state"]
    recommended_nodes = get_user_nodes(scores)
    response = Response(dumps(recommended_nodes))
    return response, 200
