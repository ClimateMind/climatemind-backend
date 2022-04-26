from flask import jsonify, request

from app.personal_values.enums import PersonalValue
from app.scoring import bp
from app.scoring.score_nodes import score_nodes
from app.errors.errors import InvalidUsageError, DatabaseError, CustomError
from app.common.uuid import validate_uuid, uuidType, check_uuid_in_db
from app.models import Scores
from flask_cors import cross_origin

from app import db, auto, cache


@bp.route("/feed", methods=["GET"])
@cross_origin()
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
    quiz_uuid = request.args.get("quizId")
    quiz_uuid = validate_uuid(quiz_uuid, uuidType.QUIZ)
    check_uuid_in_db(quiz_uuid, uuidType.QUIZ)

    session_uuid = request.headers.get("X-Session-Id")

    if not session_uuid:
        raise InvalidUsageError(message="Cannot get feed without a session ID.")

    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    feed_entries = get_feed_results(quiz_uuid, N_FEED_CARDS, session_uuid)

    return feed_entries


@cache.memoize(timeout=1200)  # 20 minutes
def get_feed_results(quiz_uuid, N_FEED_CARDS, session_uuid):
    """
    Mitigation solutions are served randomly based on a user's highest scoring climate
    impacts. The order of these should not change when a page is refreshed. This method
    looks for an existing cache based on a user's session ID, or creates a new feed if
    one is not found.
    """
    scores = db.session.query(Scores).filter_by(quiz_uuid=quiz_uuid).first()

    if scores:

        personal_values_categories = [v.key for v in PersonalValue]
        scores = scores.__dict__
        scores = {key: scores[key] for key in personal_values_categories}

        try:
            SCORE_NODES = score_nodes(scores, N_FEED_CARDS, quiz_uuid, session_uuid)
            recommended_nodes = SCORE_NODES.get_user_nodes()
            feed_entries = {"climateEffects": recommended_nodes}
            return jsonify(feed_entries), 200
        except:
            raise CustomError(
                message="Cannot get feed results. Something went wrong while processing the user's recommended nodes."
            )

    else:
        raise DatabaseError(message="Cannot get feed results. Quiz ID not in database.")
