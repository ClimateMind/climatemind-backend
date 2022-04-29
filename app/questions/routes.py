from json import dumps

from flask import Response
from flask_cors import cross_origin

from app import auto
from app.questions import bp
from app.questions.utils import get_schwartz_questions_file_data


@bp.route("/questions", methods=["GET"])
@cross_origin()
@auto.doc()
def get_questions():
    """
    Returns the list of available schwartz personal value questions that can be
    presented to the user.
    """
    data = get_schwartz_questions_file_data()
    response = Response(dumps(data))
    response.headers["Content-Type"] = "application/json"

    return response, 200
