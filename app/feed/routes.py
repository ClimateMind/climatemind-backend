from flask import jsonify, request
from app.scoring import bp
from app.scoring.score_nodes import score_nodes

from app.models import Scores

from app import db, auto, cache


@bp.route("/feed", methods=["GET"])
@auto.doc()
def get_feed():
    """
    The front-end needs to request personalized climate change effects that are most
    relevant to a user to display in the user's feed.
    PARAMETER (as GET)
    ------------------
    session-id : uuid4 as string
    """
    N_FEED_CARDS = 21

    session_id = str(request.args.get("session-id"))

    if session_id:
        feed_entries = get_feed_results(session_id, N_FEED_CARDS)
        return feed_entries
    else:
        return {"error": "No session ID provided"}, 400


@cache.memoize(timeout=1200)  # 20 minutes
def get_feed_results(session_id, N_FEED_CARDS):
    """
    Mitigation solutions are served randomly based on a user's highest scoring climate
    impacts. The order of these should not change when a page is refreshed. This method
    looks for an existing cache based on a user's session ID, or creates a new feed if
    one is not found.
    """
    scores = db.session.query(Scores).filter_by(session_id=session_id).first()

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
        scores = {key: scores[key] for key in personal_values_categories}

        SCORE_NODES = score_nodes(scores, N_FEED_CARDS, session_id)
        recommended_nodes = SCORE_NODES.get_user_nodes()
        feed_entries = {"climateEffects": recommended_nodes}
        return jsonify(feed_entries), 200

    else:
        return {"error": "Invalid session ID or no information for ID"}, 400
