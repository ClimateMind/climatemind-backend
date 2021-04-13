import os

from flask import jsonify, request

from json import load

from app.personal_values import bp

from app.models import Scores

from app import auto


@bp.route("/personal_values", methods=["GET"])
@auto.doc()
def get_personal_values():
    """
    Users want to know their personal values based on their Schwartz questionnaire
    results. This returns the top 3 personal values of a user given a session ID.
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
        all_scores = [{'personalValue': key, 'score': scores[key]}
                      for key in personal_values_categories]

        # Top 3 personal values
        top_scores = sorted(
            all_scores, key=lambda value: value['score'], reverse=True)[:3]

        print(top_scores)

        # Fetch descriptions
        try:
            file = os.path.join(
                os.getcwd(), "app/personal_values/static", "value_descriptions.json"
            )
            with open(file) as f:
                value_descriptions = load(f)
        except FileNotFoundError:
            return {"error": "Value descriptions file not found"}, 404
        # descriptions = [value_descriptions[score.personalValue]
        #                 for score in top_scores]

        # # Add descriptions to top 3 personal values
        # scores_and_descriptions = []
        # for i in range(len(top_scores)):
        #     scores_and_descriptions.append(descriptions[i])

        # Build and return response
        response = {
            # "personalValues": scores_and_descriptions,
            "personalValues": top_scores,
            "scores": all_scores
        }
        return jsonify(response), 200

    else:
        return {"error": "Invalid session ID"}, 400
