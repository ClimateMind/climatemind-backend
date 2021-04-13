import os

from flask import jsonify, request

from json import load

from app.personal_values import bp

from app.models import Scores

from app import auto


def normalize_scores(values):
    min_score = min([value["score"] for value in values])
    max_score = max([value["score"] for value in values])
    # TODO: Check this correct way to normalise scores
    for val in values:
        val["score"] = (val["score"] - min_score) / (max_score - min_score) * 10
    return values


@bp.route("/personal_values", methods=["GET"])
@auto.doc()
def get_personal_values():
    """
    Users want to know their personal values based on their Schwartz questionnaire
    results. This returns the top 3 personal values with descriptions plus all scores for a user given a session ID.
    """
    try:
        session_uuid = request.args.get("session-id")

    except:
        return {"error": "Invalid session ID format or no ID provided"}, 400

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
            return {"error": "Value descriptions file not found"}, 404
        print(top_scores)

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
        return {"error": "Invalid session ID"}, 400
