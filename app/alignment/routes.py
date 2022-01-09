import uuid

from flask import jsonify, request
from flask_cors import cross_origin

from app import auto, db
from app.alignment import bp
from app.models import Sessions
from app.errors.errors import InvalidUsageError
from app.auth.utils import check_uuid_in_db, uuidType, validate_uuid
from app.user_b.analytics_logging import log_user_b_event, eventType
from app.user_b.journey_updates import update_user_b_journey
from app.scoring.process_alignment_scores import create_alignment_scores
from app.feed.process_alignment_feed import create_alignment_feed


@bp.route("/alignment", methods=["POST"])
@cross_origin()
@auto.doc()
def post_alignment_uuid():
    """
    Post alignment. After user b has taken the quiz, their results are compared to user a and their
    aligned scores and aligned feeds are calculated. User b analytics events are saved in the db and
    the user b journey table is updated to record the user b quiz, aligned scores and aligned feed uuids.

    Parameters
    =====================
    conversationId (UUID)
    quizId (UUID) - the user b quiz uuid

    Returns
    =====================
    alignmentScoresId (UUID) - the uuid for the entry in the alignment scores table

    """
    session_uuid = request.headers.get("X-Session-Id")

    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    r = request.get_json(force=True, silent=True)

    conversation_uuid = r.get("conversationId")
    quiz_uuid = r.get("quizId")

    conversation_uuid = validate_uuid(conversation_uuid, uuidType.CONVERSATION)
    check_uuid_in_db(conversation_uuid, uuidType.CONVERSATION)
    quiz_uuid = validate_uuid(quiz_uuid, uuidType.QUIZ)
    check_uuid_in_db(quiz_uuid, uuidType.QUIZ)

    alignment_scores_uuid = uuid.uuid4()
    alignment_feed_uuid = uuid.uuid4()

    create_alignment_scores(conversation_uuid, quiz_uuid, alignment_scores_uuid)
    create_alignment_feed(conversation_uuid, quiz_uuid, alignment_feed_uuid)

    log_user_b_event(conversation_uuid, session_uuid, eventType.QUIZ, quiz_uuid)
    update_user_b_journey(
        conversation_uuid,
        quiz_uuid=quiz_uuid,
        alignment_scores_uuid=alignment_scores_uuid,
        alignment_feed_uuid=alignment_feed_uuid,
    )

    response = {"alignmentScoresId": alignment_scores_uuid}
    return jsonify(response), 201


@bp.route("/alignment/<alignment_scores_uuid>", methods=["GET"])
@cross_origin()
def get_alignment(alignment_scores_uuid):

    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    validate_uuid(alignment_scores_uuid, uuidType.ALIGNMENT_SCORES)
    check_uuid_in_db(alignment_scores_uuid, uuidType.ALIGNMENT_SCORES)

    allowed_perspectives = {"userA", "userB"}
    perspective = request.args.get("perspective")
    if (perspective not in allowed_perspectives):
        raise InvalidUsageError(
            message="The perspective parameter must be one of ({})"\
            .format(','.join(allowed_perspectives))
        )

    response = None # TODO: implement
    return jsonify(response), 200
