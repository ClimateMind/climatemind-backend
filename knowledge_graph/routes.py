from flask_swagger_ui import get_swaggerui_blueprint
from json import dumps, load
from typing import Tuple

from flask import request, make_response, Response, send_from_directory

from knowledge_graph import app, db
from knowledge_graph.persist_scores import persist_scores
from knowledge_graph.score_nodes import get_user_nodes
from knowledge_graph.models import Scores

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

score_description = {
    "conformity": "Compliance with rules, laws and formal obligations (Avoidance of violating formal social expectations)",
    "tradition": "Maintaining and preserving cultural, family and/or religious traditions",
    "universalism": "You encompass appreciation, tolerance, and general acceptance of the nature of things around you.",
    "benevolence": "Promoting the welfare of one’s in-groups by being trustworthy and reliable",
    "self-direction": "Freedom to determine one’s own actions",
    "stimulation": "Excitement, novelty, and change",
    "hedonism": "Pleasure or sensuous gratification",
    "achievement": "Success according to social standards",
    "power": "Control over people and resources",
    "security": "Safety, stability and order (security) in the wider society"    
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

    value_scores["session-id"] = session_id

    persist_scores(value_scores)

    response = Response(dumps(value_scores))
    return response, 200
    

@app.route('/personal_values', methods=['GET'])
def get_personal_values():
    """ Given a session-id, this returns the top three personal values for a user
    
    """
    session_id = int(request.args.get('session-id'))
    
    try:
        scores = db.session.query(Scores).filter_by(session_id=1).first()
    except:
        return make_response("Invalid Session ID"), 400
    
    scores = scores.__dict__
    del scores["_sa_instance_state"]
    
    top_scores = sorted(scores, key=scores.get, reverse=True)[:3]
    descriptions = [score_description[score] for score in top_scores]
    scores_and_descriptions = [list(s) for s in zip(top_scores, descriptions)]
    
    return make_response(dumps(scores_and_descriptions)), 200
    


@app.route("/get_actions", methods=["POST"])
def get_actions():
    try:
        scores = request.json
    except:
        return make_response("Invalid JSON"), 400
    recommended_nodes = get_user_nodes(scores)
    response = Response(dumps(recommended_nodes))
    return response, 200
