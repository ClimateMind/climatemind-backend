import os
from flask import jsonify, request
from json import load

from app.personal_values.enums import PersonalValue
from app.personal_values import bp
from app.models import Scores
from app.common.uuid import validate_uuid, uuidType, check_uuid_in_db

from app.personal_values.normalize import normalize_scores
from flask_cors import cross_origin

from app.personal_values.utils import get_value_descriptions_file_data


@bp.route("/personal_values", methods=["GET"])
@cross_origin()
def get_personal_values():
    """
    Users want to know their personal values based on their Schwartz questionnaire
    results. This returns the top 3 personal values with descriptions plus all scores for a user given a quiz ID.
    """
    quiz_uuid = request.args.get("quizId")
    quiz_uuid = validate_uuid(quiz_uuid, uuidType.QUIZ)
    check_uuid_in_db(quiz_uuid, uuidType.QUIZ)

    scores = Scores.query.filter_by(quiz_uuid=quiz_uuid).first()
    scores = scores.__dict__

    # All scores and associated values for response
    all_scores = [
        {"personalValue": v.key, "score": scores[v.key]} for v in PersonalValue
    ]

    normalized_scores = normalize_scores(all_scores)

    # Top 3 personal values
    top_scores = sorted(all_scores, key=lambda value: value["score"], reverse=True)[:3]

    # Fetch descriptions
    value_descriptions = get_value_descriptions_file_data()

    # Add descriptions for top 3 values to return
    values_and_descriptions = [
        value_descriptions[score["personalValue"]] for score in top_scores
    ]

    # Build and return response
    response = {
        "personalValues": values_and_descriptions,
        "valueScores": normalized_scores,
    }

    return jsonify(response), 200
