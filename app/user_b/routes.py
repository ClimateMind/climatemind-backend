from urllib import response
from app.user_b import bp
from app.user_b.analytics_logging import log_user_b_event, eventType
from app.user_b.journey_updates import start_user_b_journey
from app.auth.utils import validate_uuid, check_uuid_in_db, uuidType
from flask_cors import cross_origin
from flask import request, jsonify


@bp.route("/user-b/<conversation_uuid>", methods=["POST"])
@cross_origin()
def post_user_b_event(conversation_uuid):
    """
    Creates an entry in the user_b_journey table to start centralised storage of the most recent events/selections
    on User B's journey through the app, e.g. most recent quiz uuid and alignment uuids if the user retakes the quiz
    multiple times.

    Logs that the unique link was clicked in the user_b_analytics_data table.

    Session uuid validation is included for accurate logging.

    Parameters
    ==========
    conversation_uuid - (UUID) the unique id for the conversation

    Returns
    ==========
    JSON - success message

    """
    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    start_user_b_journey(conversation_uuid)
    log_user_b_event(conversation_uuid, session_uuid, eventType.LINK, 1)

    response = {"message": "User B clicked the link."}

    return jsonify(response), 201
