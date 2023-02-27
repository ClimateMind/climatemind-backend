from datetime import datetime, timezone

from flask import jsonify, request
from flask_cors import cross_origin
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.common.uuid import validate_uuid, uuidType, check_uuid_in_db
from app.errors.errors import DatabaseError
from app.feedback.schemas import FeedbackSchema
from app.feedback import bp


@bp.route("/feedback", methods=["POST"])
@cross_origin()
def post_feedback():
    """
    Returns HTTP codes
    -------
    200 - feedback saved successfully
    404 - session is not found
    422 - validation issue
    500 - unable to save feedback
    """

    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    json_data = request.get_json(force=True, silent=True)

    feedback = FeedbackSchema().load(json_data)

    try:
        feedback.session_uuid = session_uuid
        feedback.created = datetime.now(timezone.utc)
        db.session.add(feedback)
        db.session.commit()
    except SQLAlchemyError:  # pragma: no cover
        raise DatabaseError(message="Unable to save feedback")

    response = {"message": "OK"}
    return jsonify(response), 200
