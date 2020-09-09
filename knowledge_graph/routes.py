from json import dumps, load
from typing import Tuple

from flask import request, make_response, Response

from knowledge_graph import app
from knowledge_graph.score_nodes import get_user_nodes

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
    10: "security"
}


@app.route('/', methods=['GET'])
def home() -> Tuple[str, int]:
    return "<h1>API for climatemind ontology</h1>", 200


@app.route('/ontology', methods=['GET'])
def query() -> Tuple[Response, int]:
    searchQueries = request.args.getlist('query')

    searchResults = {}

    mind = app.config["MIND"]

    try:
        for keyword in searchQueries:
            searchResults[keyword] = mind.search(keyword)

    except ValueError:
        # todo: currently returns no results at all if 1 keyword in an array isn't found. fix this.
        return make_response("query keyword not found"), 400

    response = Response(dumps(searchResults))
    response.headers['Content-Type'] = 'application/json'

    return response, 200


@app.route('/questions', methods=['GET'])
def get_questions() -> Tuple[Response, int]:
    try:
        with open('schwartz_questions.json') as json_file:
            data = load(json_file)
    except FileNotFoundError:
        return make_response("Schwartz Questions not Found"), 400

    response = Response(dumps(data))
    response.headers['Content-Type'] = 'application/json'

    return response, 200


@app.route('/scores', methods=['POST'])
def user_scores() -> Tuple[Response, int]:
    if request.method == 'POST':
        return receive_user_scores()

def receive_user_scores() -> Tuple[Response, int]:
    """ Users want to be able to get their score results after submitting
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
    print(overall_avg)

    for value, score in value_scores.items():
        centered_score = score - overall_avg + POSITIVITY_CONSTANT # To make non-negative
        value_scores[value] = centered_score

    response = Response(dumps(value_scores))
    return response, 200

@app.route('/get_actions', methods=['POST'])
def get_actions():
    try:
        scores = request.json
    except:
        return make_response("Invalid JSON"), 400
    recommended_nodes = get_user_nodes(scores)
    response = Response(dumps(recommended_nodes))
    return response, 200
    
