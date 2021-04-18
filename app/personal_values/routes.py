import os
from flask import jsonify, request
from json import load
from app.personal_values import bp
from app.models import Scores
from app import auto
from app.errors.errors import InvalidUsageError, DatabaseError
import uuid


@bp.route("/personal_values", methods=["GET"])
@auto.doc()
def get_personal_values():
    """
    Users want to know their personal values based on their Schwartz questionnaire
    results. This returns the top 3 personal values of a user given a session ID.
    """
    try:
        session_uuid = uuid.UUID(request.args.get("session-id"))

    except:
        raise InvalidUsageError(
            message="Malformed request. Session id provided to get personal values is not a valid UUID."
        )

    scores = Scores.query.filter_by(session_uuid=session_uuid).first()

    if scores:

        personal_values_categories = [
            "security",
            "conformity",
            "benevolence",
            "tradition",
            "universalism",
            "self_direction",
            "stimulation",
            "hedonism",
            "achievement",
            "power",
        ]

        scores = scores.__dict__
        sorted_scores = {key: scores[key] for key in personal_values_categories}

        top_scores = sorted(sorted_scores, key=sorted_scores.get, reverse=True)[:3]

        try:
            file = os.path.join(
                os.getcwd(), "app/personal_values/static", "value_descriptions.json"
            )
            with open(file) as f:
                value_descriptions = load(f)
        except FileNotFoundError:
            return jsonify({"error": "Value descriptions file not found"}), 404

        descriptions = [value_descriptions[score] for score in top_scores]
        scores_and_descriptions = []

        for i in range(len(top_scores)):
            scores_and_descriptions.append(descriptions[i])
        response = {"personalValues": scores_and_descriptions}
        return jsonify(response), 200

    else:
        raise DatabaseError(
            message="Cannot get personal values. Session id is not in database."
        )
