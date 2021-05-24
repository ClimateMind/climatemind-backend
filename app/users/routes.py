from app import db
from app.users import bp
from app.models import Users, Scores, Sessions, AnalyticsData, ClimateFeed
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user
from app.errors.errors import InvalidUsageError, DatabaseError
from flask_cors import cross_origin
from flask import request, jsonify


@bp.route("/user/<user_id>", methods=["PUT"])
@cross_origin()
@jwt_required()
def update_user(user_id):
    r = request.get_json(force=True, silent=True)

    if not r:
        raise InvalidUsageError(
            message="Valid JSON body must be provided in the request."
        )

    user_uuid = current_user.uuid
    new_session_id = r.get("session-id", None)

    if not user_uuid or not new_session_id:
        raise InvalidUsageError(
            message="User UUID and Session UUID must be included in request body."
        )

    update_session(user_uuid, new_session_id)

    if session:
        new_session = Sessions(session_uuid=new_session_id)
        new_session.ip_address = session.ip_address
        new_session.postal_code = session.postal_code

    if scores:
        scores.session_uuid = new_session.session_uuid

    if feed:
        feed.session_uuid = new_session.session_uuid

    if analytics:
        analytics.session_uuid = new_session.session_uuid

    try:
        db.session.add(new_session)
        db.session.delete(session)
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while adding the session to the database."
        )

    return (
        jsonify(
            {
                "message": "Successfully updated the session-id.",
                "session-id": new_session_id,
                "old-session-id": old_session_id,
            }
        ),
        200,
    )


def create_session(user_uuid, new_session_id):
    try:
        scores = db.session.query(Scores).filter_by(user_uuid=user_uuid).one_or_none()

    except:
        raise DatabaseError(message="An error occurred while querying the database.")
