from crypt import methods
import json
from time import perf_counter
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
from app.alignment.utils import *


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
    create_alignment_feed(conversation_uuid, quiz_uuid, alignment_feed_uuid, alignment_scores_uuid)

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
    """
    Get alignment scores.

    Includes validation of the session uuid and aligment scores uuid that they are formatted
    correctly and exist in the DB. All scores are given as integer percentages.

    Parameters
    ==========
    alignment_scores_uuid - (UUID) the unique id for the alignment scores

    Returns
    ==========
    JSON:
    - overall similarity score
    - alignment scores for all values, along with their properties
    - top value and score from the alignment scores
    - user a's first name
    - user b's name
    """

    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    validate_uuid(alignment_scores_uuid, uuidType.ALIGNMENT_SCORES)
    check_uuid_in_db(alignment_scores_uuid, uuidType.ALIGNMENT_SCORES)

    response = build_alignment_scores_response(alignment_scores_uuid)
    return jsonify(response), 200


@bp.route("/alignment/<alignment_scores_uuid>/shared-impacts", methods=["GET"])
@cross_origin()
@auto.doc()
def get_shared_impacts(alignment_scores_uuid):
    """
    Get a list of the shared impacts generated by comparing user A's and user B's quiz scores.

    Includes validation of the session uuid and alignment scores uuid that they are formatted
    correctly and exist in the db.

    Parameters
    ==========
    alignment_scores_uuid - (UUID) the unique id for the alignment scores

    Returns
    ==========
    JSON:
    - the id, shared score, short description, title, image url (if available), and associated
    personal value(s) for each shared impact
    - user a's first name
    - user b's name
    """
    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    alignment_scores_uuid = validate_uuid(
        alignment_scores_uuid, uuidType.ALIGNMENT_SCORES
    )
    check_uuid_in_db(alignment_scores_uuid, uuidType.ALIGNMENT_SCORES)

    response = build_shared_impacts_response(alignment_scores_uuid)

    return jsonify(response), 200


@bp.route("/alignment/<alignment_scores_uuid>/shared-solutions", methods=["GET"])
@cross_origin()
@auto.doc()
def get_shared_solutions(alignment_scores_uuid):
    """
    Get a list of the shared solutions generated by comparing user A's and user B's quiz scores.

    Includes validation of the session uuid and alignment scores uuid that they are formatted
    correctly and exist in the db.

    Parameters
    ==========
    alignment_scores_uuid - (UUID) the unique id for the alignment scores

    Returns
    ==========
    JSON:
    - the id, shared score, short description, title, and image url (if available) for each shared
    solution
    - user a's first name
    - user b's name
    """

    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    alignment_scores_uuid = validate_uuid(
        alignment_scores_uuid, uuidType.ALIGNMENT_SCORES
    )
    check_uuid_in_db(alignment_scores_uuid, uuidType.ALIGNMENT_SCORES)

    response = build_shared_solutions_response(alignment_scores_uuid)

    return jsonify(response), 200


@bp.route("/alignment/<alignment_scores_uuid>/shared-impacts", methods=["POST"])
@cross_origin()
@auto.doc()
def post_shared_impact_selection(alignment_scores_uuid):
    """
    Records the shared impact that user b has selected to discuss with user a.

    Includes validation of the session uuid and alignment scores uuid that they are formatted
    correctly and exist in the db.

    Parameters
    ==========
    alignment_scores_uuid - (UUID) the unique id for the alignment scores

    Returns
    ==========
    JSON - success message or error

    """

    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    alignment_scores_uuid = validate_uuid(
        alignment_scores_uuid, uuidType.ALIGNMENT_SCORES
    )
    check_uuid_in_db(alignment_scores_uuid, uuidType.ALIGNMENT_SCORES)

    conversation_uuid = get_conversation_uuid_using_alignment_scores_uuid(
        alignment_scores_uuid
    )

    shared_impacts = request.get_json(force=True, silent=True)

    # TODO Logic will need to be rewritten if the user is later allowed to select more than one impact.
    effect_iri = shared_impacts["sharedImpacts"][0]["effectId"]

    effect_choice_uuid = uuid.uuid4()
    log_effect_choice(effect_choice_uuid, effect_iri)
    log_user_b_event(
        conversation_uuid, session_uuid, eventType.EFFECT, effect_choice_uuid
    )
    update_user_b_journey(conversation_uuid, effect_choice_uuid=effect_choice_uuid)

    response = {"message": "Shared impact saved to the db."}

    return jsonify(response), 201


@bp.route("/alignment/<alignment_scores_uuid>/shared-solutions", methods=["POST"])
@cross_origin()
@auto.doc()
def post_shared_solution_selection(alignment_scores_uuid):
    """
    Records the shared solutions that user b has selected to discuss with user a.

    Includes validation of the session uuid and alignment scores uuid that they are formatted
    correctly and exist in the db.

    Parameters
    ==========
    alignment_scores_uuid - (UUID) the unique id for the alignment scores

    Returns
    ==========
    JSON - success message or error

    """

    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    alignment_scores_uuid = validate_uuid(
        alignment_scores_uuid, uuidType.ALIGNMENT_SCORES
    )
    check_uuid_in_db(alignment_scores_uuid, uuidType.ALIGNMENT_SCORES)

    conversation_uuid = get_conversation_uuid_using_alignment_scores_uuid(
        alignment_scores_uuid
    )

    shared_solutions = request.get_json(force=True, silent=True)
    shared_solutions = shared_solutions["sharedSolutions"]

    solution_choice_uuid = uuid.uuid4()

    log_solution_choice(solution_choice_uuid, shared_solutions)
    log_user_b_event(
        conversation_uuid, session_uuid, eventType.SOLUTION, solution_choice_uuid
    )
    update_user_b_journey(conversation_uuid, solution_choice_uuid=solution_choice_uuid)

    response = {"message": "Shared solutions saved to the db."}

    return jsonify(response), 201


@bp.route("/alignment/shared-impact/<impact_iri>", methods=["GET"])
@cross_origin()
@auto.doc()
def get_shared_impact_details(impact_iri):
    """
    Gets the details for a shared impact when the user clicks Learn More on the card in their feed.
    Parameters
    ==========
    impact_iri - the IRI for the shared impact
    Returns
    ==========
    JSON:
    - the effect title
    - the image url (if available)
    - the long description for the effect
    - the sources for the effect
    - a list of personal values that are related to the effect
    """

    response = build_shared_impact_details_response(impact_iri)

    return jsonify(response), 200


@bp.route("/alignment/shared-solution/<solution_iri>", methods=["GET"])
@cross_origin()
@auto.doc()
def get_shared_solution_details(solution_iri):
    """
    Gets the details for a shared solution when the user clicks Learn More on the card in their feed.
    Parameters
    ==========
    solution_iri - the IRI for the shared solution
    Returns
    ==========
    JSON:
    - the solution title
    - the image url (if available)
    - the long description for the solution
    - the sources for the solution
    - the solution type
    """

    response = build_shared_solution_details_response(solution_iri)

    return jsonify(response), 200


@bp.route("/alignment/<alignment_scores_uuid>/summary", methods=["GET"])
@cross_origin()
@auto.doc()
def get_alignment_summary(alignment_scores_uuid):
    """
    Gets the alignment summary for user B to see before confirming their consent to share with user A.

    Parameters
    ==========
    alignment_scores_uuid - (UUID) the unique id for the alignment scores

    Returns
    ==========
    JSON:
    - user A's name
    - the top match value
    - the alignment percentage for the top match value
    - the chosen shared impact(s) title
    - the chosen shared solutions' titles
    """

    alignment_scores_uuid = validate_uuid(
        alignment_scores_uuid, uuidType.ALIGNMENT_SCORES
    )
    check_uuid_in_db(alignment_scores_uuid, uuidType.ALIGNMENT_SCORES)

    response = build_alignment_summary_response(alignment_scores_uuid)

    return jsonify(response), 200
