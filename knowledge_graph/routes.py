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
    """
    Gets the ontology.
    ---
    get:
      description: Resource for accessing the contents of the ontology via queries.
      parameters:
        - name: query
          in: query
          required: false
          style: form
          explode: true
          schema:
            type: string
          example: coal%20mining
      responses:
        "200":
          description: Successful query.
        "400":
          description: Query keyword was not found in the ontology.
          content:
            text/html; charset=utf-8:
              schema:
                type: string
              examples: {}
    :return:
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
def get_questions() -> Tuple[Response, int]:
    """
    Get list of questions
    ---
    get:
      description:
        Returns the list of available questions that can be presented to
        the user.
      responses:
        "200":
          description: Successful get_questions response.
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/inline_response_200"
              examples:
                "0":
                  value:
                    '{"SetOne": [{"id": 1, "value": "conformity", "question":
                    "They believe they should always show respect to their parents
                    and to older people. It is important to them to be obedient."},
                    {"id": 2, "value": "tradition", "question": "Religious belief
                    or traditions are important to them. They try hard to do what
                    their religion or family traditions require."}, {"id": 3, "value":
                    "benevolence", "question": "It''s very important to them to help
                    the people around them. They want to care for the well-being of
                    those around them."}, {"id": 4, "value": "universalism", "question":
                    "They think it is important that every person in the world be
                    treated equally. They believe everyone should have equal opportunities
                    in life."}, {"id": 5, "value": "self-direction", "question": "They
                    think it''s important to be interested in things. They like to
                    be curious and to try to understand all sorts of things."}, {"id":
                    6, "value": "stimulation", "question": "They like to take risks.
                    They are always looking for adventures."}, {"id": 7, "value":
                    "hedonism", "question": "They seek every chance they can to have
                    fun. It is important to them to do things that give them pleasure."},
                    {"id": 8, "value": "achievement", "question": "Being very successful
                    is important to them. They like to impress other people."}, {"id":
                    9, "value": "power", "question": "It is important to them to be
                    in charge and tell others what to do. They want people to do what
                    they say."}, {"id": 10, "value": "security", "question": "It is
                    important to them that things be organized and clean. They really
                    do not like things to be a mess."}], "SetTwo": [{"id": 1, "value":
                    "conformity", "question": "It is important to they to always behave
                    properly. They want to avoid doing anything people would say is
                    wrong."}, {"id": 2, "value": "tradition", "question": "They think
                    it is best to do things in traditional ways. It is important to
                    they to keep up the customs they have learned."}, {"id": 3, "value":
                    "benevolence", "question": "It is important to them to respond
                    to the needs of others. They try to support those they know."},
                    {"id": 4, "value": "universalism", "question": "They believe all
                    the worlds'' people should live in harmony. Promoting peace among
                    all groups in the world is important to them."}, {"id": 5, "value":
                    "self-direction", "question": "Thinking up new ideas and being
                    creative is important to them. They like to do things in their
                    own original way."}, {"id": 6, "value": "stimulation", "question":
                    "They think it is important to do lots of different things in
                    life. they always look for new things to try."}, {"id": 7, "value":
                    "hedonism", "question": "They really want to enjoy life. Having
                    a good time is very important to them."}, {"id": 8, "value": "achievement",
                    "question": "Getting ahead in life is important to them. They
                    strive to do better than others."}, {"id": 9, "value": "power",
                    "question": "They always want to be the one who makes the decisions.
                    They like to be the leader."}, {"id": 10, "value": "security",
                    "question": "Having a stable government is important to them.
                    They are concerned that the social order be protected."}], "Answers":
                    [
                        {
                            "id": 1,
                            "text": "Not Like Me At All"
                        },
                        {
                            "id": 2,
                            "text": "Not Like Me"
                        },
                        {
                            "id": 3,
                            "text": "Little Like Me"
                        },
                        {
                            "id": 4,
                            "text": "Somewhat Like Me"
                        },
                        {
                            "id": 5,
                            "text": "Like Me"
                        },
                        {
                            "id": 6,
                            "text": "Very Much Like Me"
                        }
                    
                    , "Directions": "Here we briefly describe different people.
                    Please read each description and think about how much that person
                    is or is not like you."}'
    :return: 
    """
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
    """
    Get info on our server
    ---
    post:
      description: |-
        Users want to be able to get their score results after submitting the survey.
        The user can answer 10 or 20 questions. If they answer 20, the scores are averaged between the 10 additional and 10 original questions to get 10 corresponding value scores.
        Then to get a centered score for each value, each score value is subtracted from the overall average of all 10 or 20 questions. This score is returned in the response.
      requestBody:
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/body"
            examples:
              "0":
                value:
                  {
                    "SetOne":
                      [
                        {
                          "id": 1,
                          "value": "conformity",
                          "question": "They believe they should always show respect to their parents and to older people. It is important to them to be obedient.",
                        },
                        {
                          "id": 2,
                          "value": "tradition",
                          "question": "Religious belief or traditions are important to them. They try hard to do what their religion or family traditions require.",
                        },
                        {
                          "id": 3,
                          "value": "benevolence",
                          "question": "It's very important to them to help the people around them. They want to care for the well-being of those around them.",
                        },
                        {
                          "id": 4,
                          "value": "universalism",
                          "question": "They think it is important that every person in the world be treated equally. They believe everyone should have equal opportunities in life.",
                        },
                        {
                          "id": 5,
                          "value": "self-direction",
                          "question": "They think it's important to be interested in things. They like to be curious and to try to understand all sorts of things.",
                        },
                        {
                          "id": 6,
                          "value": "stimulation",
                          "question": "They like to take risks. They are always looking for adventures.",
                        },
                        {
                          "id": 7,
                          "value": "hedonism",
                          "question": "They seek every chance they can to have fun. It is important to them to do things that give them pleasure.",
                        },
                        {
                          "id": 8,
                          "value": "achievement",
                          "question": "Being very successful is important to them. They like to impress other people.",
                        },
                        {
                          "id": 9,
                          "value": "power",
                          "question": "It is important to them to be in charge and tell others what to do. They want people to do what they say.",
                        },
                        {
                          "id": 10,
                          "value": "security",
                          "question": "It is important to them that things be organized and clean. They really do not like things to be a mess.",
                        },
                      ],
                    "SetTwo":
                      [
                        {
                          "id": 1,
                          "value": "conformity",
                          "question": "It is important to they to always behave properly. They want to avoid doing anything people would say is wrong.",
                        },
                        {
                          "id": 2,
                          "value": "tradition",
                          "question": "They think it is best to do things in traditional ways. It is important to they to keep up the customs they have learned.",
                        },
                        {
                          "id": 3,
                          "value": "benevolence",
                          "question": "It is important to them to respond to the needs of others. They try to support those they know.",
                        },
                        {
                          "id": 4,
                          "value": "universalism",
                          "question": "They believe all the worlds' people should live in harmony. Promoting peace among all groups in the world is important to them.",
                        },
                        {
                          "id": 5,
                          "value": "self-direction",
                          "question": "Thinking up new ideas and being creative is important to them. They like to do things in their own original way.",
                        },
                        {
                          "id": 6,
                          "value": "stimulation",
                          "question": "They think it is important to do lots of different things in life. they always look for new things to try.",
                        },
                        {
                          "id": 7,
                          "value": "hedonism",
                          "question": "They really want to enjoy life. Having a good time is very important to them.",
                        },
                        {
                          "id": 8,
                          "value": "achievement",
                          "question": "Getting ahead in life is important to them. They strive to do better than others.",
                        },
                        {
                          "id": 9,
                          "value": "power",
                          "question": "They always want to be the one who makes the decisions. They like to be the leader.",
                        },
                        {
                          "id": 10,
                          "value": "security",
                          "question": "Having a stable government is important to them. They are concerned that the social order be protected.",
                        },
                      ],
                    "Answers": [
                        {
                            "id": 1,
                            "text": "Not Like Me At All"
                        },
                        {
                            "id": 2,
                            "text": "Not Like Me"
                        },
                        {
                            "id": 3,
                            "text": "Little Like Me"
                        },
                        {
                            "id": 4,
                            "text": "Somewhat Like Me"
                        },
                        {
                            "id": 5,
                            "text": "Like Me"
                        },
                        {
                            "id": 6,
                            "text": "Very Much Like Me"
                        }
                    ],
                    "Directions": "Here we briefly describe different people. Please read each description and think about how much that person is or is not like you.",
                  }
      responses:
        "200":
          description: Successful get_user_scores response.
          content:
            text/html; charset=utf-8:
              schema:
                type: string
              examples: {}
    :return:
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


# add your
with app.test_request_context():
    spec.path(view=get_actions)
    spec.path(view=get_personal_values)
    spec.path(view=user_scores)
    spec.path(view=get_questions)
    spec.path(view=query)
    spec.path(view=get_feed)


@app.route("/spec")
def get_apispec():
    return jsonify(spec.to_dict())
