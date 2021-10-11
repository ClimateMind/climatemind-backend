import uuid

from flask import jsonify, request
from flask_cors import cross_origin
from sqlalchemy.exc import SQLAlchemyError

from app import auto, cache, db
from . import bp
from .get_feed import GetFeed
from .store_climate_feed_data import store_climate_feed_data
from ..auth.utils import check_uuid_in_db, uuidType, validate_uuid
from ..errors.errors import CustomError, DatabaseError, InvalidUsageError
from ..models import Sessions, Scores
from ..myths.process_myths import process_myths
from ..network_x_tools.network_x_utils import network_x_utils
from ..solutions.process_solutions import process_solutions


@bp.route("/feed", methods=["GET"])
@cross_origin()
@auto.doc()
def get_feed():
    """
    Provides the user with climate change effects that are most
    personalized to display in the user's feed.

    :param quizId: uuid4 as string (passed via url arg)

    :returns: Feed data as JSON & 200 on success
    """
    num_feed_cards = 21                     # Planned for more use, do not move
    quiz_uuid = request.args.get("quizId")
    quiz_uuid = validate_uuid(quiz_uuid, uuidType.QUIZ)
    check_uuid_in_db(quiz_uuid, uuidType.QUIZ)

    session_uuid = request.headers.get("X-Session-Id")

    if not session_uuid:
        raise InvalidUsageError(message="Cannot get feed without a session ID.")

    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    feed_entries = get_feed_results(quiz_uuid, session_uuid, num_feed_cards)

    return jsonify(feed_entries), 200


@cache.memoize(timeout=1200)  # 20 minutes
def get_feed_results(quiz_uuid, session_uuid, num_feed_cards):
    """
    Mitigation solutions are served randomly based on a user's highest scoring climate
    impacts. The order of these should not change when a page is refreshed. This method
    looks for an existing cache based on a user's session ID, or creates a new feed if
    one is not found.

    :param quiz_uuid: uuid4 as string
    :param session_uuid: uuid4 as string
    :param num_feed_cards: int

    :returns feed_entries: dictionary of feed data
    """
    scores = db.session.query(Scores).filter_by(quiz_uuid=quiz_uuid).first()

    if not scores:
        raise DatabaseError(message="Cannot get feed results. Quiz ID not in database.")

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

    node_scoring = GetFeed(scores)

    nx_utils = network_x_utils()
    myth_processor = process_myths()
    solution_processor = process_solutions()
    node_scoring.score_nodes(session_uuid, nx_utils, myth_processor, solution_processor)

    recommended_nodes = node_scoring.get_best_nodes(num_feed_cards)

    try:
        store_climate_feed_data(session_uuid, recommended_nodes)

    except SQLAlchemyError:
        raise DatabaseError(message="Cannot store the results to the DB.")

    feed_entries = {"climateEffects": recommended_nodes}

    return feed_entries
