import os
from json import dumps, load
from app.questions import bp
from flask import Response

from app import auto


@bp.route("/questions", methods=["GET"])
@auto.doc()
def get_questions():
    """
    Returns the list of available schwartz personal value questions that can be
    presented to the user.
    """
    try:
        file = os.path.join(
            os.getcwd(), "app/questions/static", "schwartz_questions.json"
        )
        with open(file) as json_file:
            data = load(json_file)
    except FileNotFoundError:
        return {"error": "Schwartz questions not found"}, 404

    response = Response(dumps(data))
    response.headers["Content-Type"] = "application/json"

    return response, 200
