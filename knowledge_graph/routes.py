from knowledge_graph import app

import json

from json import dumps

from flask import request, make_response, abort, Response

from knowledge_graph.Mind import Mind


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
    

@app.route('/get_questions', methods=['GET'])
def get_questions():
    try:
        with open('schwartz_questions.json') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        return make_response("Schwartz Questions not Found"), 400
    
    response = Response(dumps(data))
    response.headers['Content-Type'] = 'application/json'
    
    return response, 200
        
    
