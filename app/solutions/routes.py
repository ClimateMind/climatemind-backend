from flask import jsonify, request
from app import db
from app.models import Scores
from app.solutions import bp
from app.solutions.process_solutions import process_solutions
from app.errors.errors import InvalidUsageError, CustomError
from flask_cors import cross_origin
import numpy as np
import pickle
import uuid

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
    session_id = request.args.get("session-id")
    user_scores = None

    if session_id:
        try:
            session_id = uuid.UUID(request.args.get("session-id"))
            user_scores = [np.array(get_scores_vector(session_id))]
        except:
            raise InvalidUsageError(
                message="Malformed request. Session id provided to get solutions is not a valid UUID."
            )

    if user_scores:
        user_liberal, user_conservative = predict_radical_political(user_scores)
    else:
        user_liberal, user_conservative = None, None

    try:
        recommended_general_solutions = (
            SOLUTION_PROCESSOR.get_user_general_solution_nodes(
                user_liberal, user_conservative
            )
        )
        climate_general_solutions = {"solutions": recommended_general_solutions}
        return jsonify(climate_general_solutions), 200

    except:
        raise CustomError(
            message="An error occurred while processing the user's general solution nodes."
        )


def predict_radical_political(user_scores):
    """
    Predicts whether or not the user is radically liberal or radically conservative

    Args:
        user_scores: A 2D array containing the user's value scores

    Returns: Booleans for liberal and conservative ex. (1, 0)

    """
    try:
        liberal_model = pickle.load(
            open(
                "ml_models/political_preference/models/NaiveBayes_liberal_0.641.pickle",
                "rb",
            )
        )
        user_liberal = liberal_model.predict(user_scores)

        conservative_model = pickle.load(
            open(
                "ml_models/political_preference/models/NaiveBayes_conservative_0.586.pickle",
                "rb",
            )
        )
        user_conservative = conservative_model.predict(user_scores)

        return user_liberal, user_conservative

    except pickle.PickleError:
        raise CustomError(message="Pickle Error when processing ml models")


def get_scores_vector(session_id):
    """
    Finds user scores in the database based on session_id

    Args:
        session_id: (str) UUID4

    Returns: A vector of scores (or None if user not found)

    """
    try:
        scores = (
            db.session.query(Scores).filter_by(session_uuid=session_id).one_or_none()
        )
        if scores:
            return [
                scores.achievement,
                scores.benevolence,
                scores.conformity,
                scores.hedonism,
                scores.power,
                scores.security,
                scores.self_direction,
                scores.stimulation,
                scores.tradition,
                scores.universalism,
            ]
        else:
            return None
    except:
        raise DatabaseError(
            message="Cannot get scores based on session_id. Failed to query database."
        )
