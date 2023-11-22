from app.analytics.analytics_logging import log_user_a_event
from app.common.uuid import validate_uuid, uuidType, check_uuid_in_db
from flask_cors import cross_origin
from flask import request, jsonify

import uuid
from datetime import datetime
from app.analytics.schemas import (
    AnalyticsSchema,
)


@bp.route("/analytics", methods=["POST"])
@cross_origin()
def post_user_a_event(conversation_uuid):
    """
    Logs a user a event in the analytics_data table for analytics tracking.

    The required request body must include category, action, label, session_uuid, event_timestamp, value, page_url

    Session uuid validation are included for accurate logging.

    Parameters
    ==========
    (implicitly session_uuid), category, action, label, session_uuid, event_timestamp, value, page_url

    Returns
    ==========
    JSON - success message

    """

    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    json_data = request.get_json(force=True, silent=True)
    schema = LoggedUserDeleteAccountSchema()
    result_data = schema.load(json_data)
    log_user_a_event(session_uuid,result_data["category"],result_data["action"],result_data["label"],result_data["event_value"],result_data["event_timestamp"],result_data["page_url"])

    response = {"message": "User event logged."}

    return jsonify(response), 201



