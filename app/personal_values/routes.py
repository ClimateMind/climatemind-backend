import os
from flask import jsonify, request
from json import load

from app.personal_values.enums import PersonalValue
from app.personal_values import bp
from app.models import Scores
from app.common.uuid import validate_uuid, uuidType, check_uuid_in_db
from app import auto

from app.personal_values.normalize import normalize_scores
from flask_cors import cross_origin


@bp.route("/personal_values", methods=["GET"])
@cross_origin()
@auto.doc()
def get_personal_values():
    """
    Users want to know their personal values based on their Schwartz questionnaire
    results. This returns the top 3 personal values with descriptions plus all scores for a user given a quiz ID.
    """
    quiz_uuid = request.args.get("quizId")
    quiz_uuid = validate_uuid(quiz_uuid, uuidType.QUIZ)
    check_uuid_in_db(quiz_uuid, uuidType.QUIZ)

    scores = Scores.query.filter_by(quiz_uuid=quiz_uuid).first()

    personal_values_categories = [
        PersonalValue.SECURITY.key,
        PersonalValue.CONFORMITY.key,
        PersonalValue.BENEVOLENCE.key,
        PersonalValue.TRADITION.key,
        PersonalValue.UNIVERSALISM.key,
        PersonalValue.SELF_DIRECTION.key,
        PersonalValue.STIMULATION.key,
        PersonalValue.HEDONISM.key,
        PersonalValue.ACHIEVEMENT.key,
        PersonalValue.POWER.key,
    ]

    scores = scores.__dict__

    # All scores and associated values for response
    all_scores = [
        {"personalValue": key, "score": scores[key]}
        for key in personal_values_categories
    ]

    normalized_scores = normalize_scores(all_scores)

    # Top 3 personal values
    top_scores = sorted(all_scores, key=lambda value: value["score"], reverse=True)[:3]

    # Fetch descriptions
    try:
        file = os.path.join(
            os.getcwd(), "app/personal_values/static", "value_descriptions.json"
        )
        with open(file) as f:
            value_descriptions = load(f)
    except FileNotFoundError:
        return jsonify({"error": "Value descriptions file not found"}), 404

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
