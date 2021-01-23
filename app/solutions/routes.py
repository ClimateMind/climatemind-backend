from flask import jsonify, request
from app.solutions import bp
from app.solutions.process_solutions import process_solutions

from app import auto

SOLUTION_PROCESSOR = process_solutions(4, 0.5)


@bp.route("/get_actions", methods=["GET"])
@auto.doc()
def get_actions():
    """
    The front-end needs to request personalized actions to take against climate change
    based on a specified climate effect.
    """
    effect_name = str(request.args.get("effect-name"))

    try:
        actions = SOLUTION_PROCESSOR.get_user_actions(effect_name)
    except:
        return {"error": "Invalid climate effect or no actions found"}, 400

    response = jsonify({"actions": actions})
    return response, 200


@bp.route("/solutions", methods=["GET"])
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
        return {"error": "Failed to process general solutions"}, 500
