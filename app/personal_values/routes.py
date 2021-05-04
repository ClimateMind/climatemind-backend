import os
from flask import jsonify, request
from json import load
from app.personal_values import bp
from app.models import Scores
from app import auto
from app.errors.errors import InvalidUsageError, DatabaseError
import uuid

from app.personal_values.normalize import normalize_scores
from flask_cors import cross_origin


@bp.route("/personal_values", methods=["GET"])
@cross_origin()
@auto.doc()
def get_personal_values():
    """
    Users want to know their personal values based on their Schwartz questionnaire
    results. This returns the top 3 personal values with descriptions plus all scores for a user given a session ID.
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

        # All scores and accoiated values for response
        all_scores = [
            {"personalValue": key, "score": scores[key]}
            for key in personal_values_categories
        ]

        normalized_scores = normalize_scores(all_scores)

        # Top 3 personal values
        top_scores = sorted(all_scores, key=lambda value: value["score"], reverse=True)[
            :3
        ]

        # Fetch descriptions
        try:
            file = os.path.join(
                os.getcwd(), "app/personal_values/static", "value_descriptions.json"
            )
            with open(file) as f:
                value_descriptions = load(f)
        except FileNotFoundError:
            return jsonify({"error": "Value descriptions file not found"}), 404

        # Add desciptions for top 3 values to retrun
        values_and_descriptions = [
            value_descriptions[score["personalValue"]] for score in top_scores
        ]

        # Build and return response
        response = {
            "personalValues": values_and_descriptions,
            "valueScores": normalized_scores,
        }
        return jsonify(response), 200

    else:
        raise DatabaseError(
            message="Cannot get personal values. Session id is not in database."
        )
