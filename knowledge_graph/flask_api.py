from json import dumps

from flask import request, make_response, abort, Response, Flask

from src.knowledge_graph import make_network
from src.knowledge_graph.mind import Mind

def abort_if_mind_doesnt_exist(m: Mind):
    if m.get_ontology() is None:
        abort(404)


app = Flask(__name__)
app.config["DEBUG"] = True


m = Mind("./climate_mind_ontology")  # TODO: pass this in as an environment variable


@app.route('/', methods=['GET'])
def home():
    return "<h1>API for climatemind ontology</h1>"


@app.route('/ontology', methods=['GET'])
def query():
    searchQuery = request.args.get('query')

    abort_if_mind_doesnt_exist(m)

    try:
        # passes ontology held in mind class to searchNode
        searchResults = make_network.searchNode(m.get_ontology(), searchQuery)
    except AttributeError:
        return make_response("query keyword not found"), 400

    response = Response(dumps(searchResults))
    response.headers['Content-Type'] = 'application/json'
    return response, 200


