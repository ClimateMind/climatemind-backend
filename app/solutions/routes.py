from flask import jsonify, request
from app.solutions import bp
from app.solutions.process_solutions import process_solutions
from app.errors.errors import InvalidUsageError, CustomError
from flask_cors import cross_origin

from app import auto

SOLUTION_PROCESSOR = process_solutions(4, 0.5)


@bp.route("/get_actions", methods=["GET"])
@cross_origin()
@auto.doc()
def get_actions():
    """
    The front-end needs to request actions to take against climate change
    based on a specified climate effect in the user's personalized feed.
    """
    effect_name = str(request.args.get("effect-name"))

    try:
        actions = SOLUTION_PROCESSOR.get_user_actions(effect_name)
    except:
        raise CustomError(message="This endpoint is not currently in use.")

    response = jsonify({"actions": actions})
    return response, 200


@bp.route("/solutions", methods=["GET"])
@cross_origin()
@auto.doc()
def get_general_solutions():
    """
    The front-end needs general solutions list and information to serve to user when
    they click the general solutions menu button. General solutions are ordered based
    on relevance predicted from users personal values.
    """
    try:
        recommended_general_solutions = (
            SOLUTION_PROCESSOR.get_user_general_solution_nodes()
        )
        climate_general_solutions = {"solutions": recommended_general_solutions}
        return jsonify(climate_general_solutions), 200
    except:
        raise CustomError(
            message="An error occurred while processing the user's general solution nodes."
        )
