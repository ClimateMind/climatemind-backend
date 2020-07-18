from json import dumps

from flask import request, make_response, abort, Response, Flask

from knowledge_graph.Mind import Mind

app = Flask(__name__)


class BaseConfig(object):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    try:
        app.config["MIND"] = Mind()
    except (FileNotFoundError, IsADirectoryError, ValueError):
        abort(404)


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    # todo: add mock mind here


@app.route('/', methods=['GET'])
def home():
    return "<h1>API for climatemind ontology</h1>"


@app.route('/ontology', methods=['GET'])
def query():
    searchQueries = request.args.getlist('query')

    searchResults = {}

    mind = app.config["MIND"]

    try:
        for keyword in searchQueries:
            searchResults[keyword] = mind.search(keyword)

    except ValueError:
        #todo: currently returns no results at all if 1 keyword in an array isn't found. fix this.
        return make_response("query keyword not found"), 400

    response = Response(dumps(searchResults))
    response.headers['Content-Type'] = 'application/json'
    return response, 200
