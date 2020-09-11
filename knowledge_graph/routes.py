from knowledge_graph import app
import json
from json import dumps, load
from flask import request, make_response, abort, Response
from typing import Tuple
from knowledge_graph.Mind import Mind
from knowledge_graph.score_nodes import get_user_nodes
from flask_login import current_user, login_user
from knowledge_graph.models import User
from knowledge_graph.forms import LoginForm

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
@app.route('/index', methods=['GET'])
def home() -> Tuple[str, int]:
    return "<h1>API for climatemind ontology</h1>", 200
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
        
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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


@app.route('/users/scores', methods=['GET', 'POST'])
def user_scores() -> Tuple[Response, int]:
    if request.method == 'GET':
        return send_user_scores()
    if request.method == 'POST':
        return receive_user_scores()


def send_user_scores() -> Tuple[Response, int]:
    return Response(dumps("placeholder score")), 200


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

    for value in parameter["SetOne"]:
        id = value["id"]
        score = value["score"]
        overall_sum += score
        value_scores[value_id_map[id]] = score

    if parameter["SetTwo"]:
        num_of_responses += 10
        for value in parameter["SetTwo"]:
            id = value["id"]
            score = value["score"]
            name = value_id_map[id]
            avg_score = (value_scores[name] + score) / 2
            overall_sum += score
            value_scores[name] = avg_score

    overall_avg = overall_sum / num_of_responses
    print(overall_avg)

    for value, score in value_scores.items():
        centered_score = score - overall_avg + 3.5 # To make non-negative
        value_scores[value] = centered_score

    response = Response(dumps(value_scores))
    return response, 200

@app.route('/get_actions', methods=['POST'])
def get_actions():
    try:
        user_scores = request.json
    except:
        return make_response("Invalid JSON"), 400
    recommended_nodes = get_user_nodes(user_scores)
    response = Response(dumps(recommended_nodes))
    return response, 200
    
