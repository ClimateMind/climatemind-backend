import uuid

from flask import jsonify, request
from flask_cors import cross_origin

from app import auto, db
from app.alignment import bp
from app.models import Sessions
from app.errors.errors import InvalidUsageError
from app.auth.utils import check_uuid_in_db, uuidType, validate_uuid


@bp.route("/alignment", methods=["POST"])
@cross_origin()
@auto.doc()
def post_alignment_uuid():
    session_uuid = request.headers.get("X-Session-Id")

    if not session_uuid:
        raise InvalidUsageError(
            message="Cannot post alignment ID without a session ID."
        )

    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    alignment_uuid = uuid.uuid4()
    response = {"alignmentId": alignment_uuid}
    return jsonify(response), 201
