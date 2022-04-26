from app.user_b import bp
from app.user_b.analytics_logging import log_user_b_event, eventType
from app.user_b.journey_updates import start_user_b_journey
from app.common.uuid import validate_uuid, uuidType, check_uuid_in_db
from flask_cors import cross_origin
from flask import request, jsonify


@bp.route("/user-b/<conversation_uuid>", methods=["POST"])
@cross_origin()
def post_user_b_event(conversation_uuid):
    """
    Logs a user b event in the user_b_analytics_data table for analytics tracking.

    The (optional) request body must include the eventType and the eventValue.

    If there is no request body:
    - Creates an entry in the user_b_journey table to start centralised storage of the most recent events/selections
    on User B's journey through the app, e.g. most recent quiz uuid and alignment uuids if the user retakes the quiz
    multiple times.
    - Logs that the unique link was clicked.

    Session uuid and conversation uuid validation are included for accurate logging.

    Parameters
    ==========
    conversation_uuid - (UUID) the unique id for the conversation

    Returns
    ==========
    JSON - success message

    """

    event = request.get_json(force=True, silent=True)

    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    conversation_uuid = validate_uuid(conversation_uuid, uuidType.CONVERSATION)
    check_uuid_in_db(conversation_uuid, uuidType.CONVERSATION)

    if event:
        event_type = event["eventType"]
        event_value = event["eventValue"]

        if event_type == "learn more - impact":
            log_user_b_event(
                conversation_uuid, session_uuid, eventType.LMEFFECT, event_value
            )
        elif event_type == "learn more - solution":
            log_user_b_event(
                conversation_uuid, session_uuid, eventType.LMSOLUTION, event_value
            )
    else:
        start_user_b_journey(conversation_uuid)
        log_user_b_event(conversation_uuid, session_uuid, eventType.LINK, 1)

    response = {"message": "User B event logged."}

    return jsonify(response), 201
