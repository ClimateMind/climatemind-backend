import datetime
import uuid
from datetime import timezone

from flask import jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required

from app import auto
from app.session import bp
from app.session.session_helpers import get_ip_address, store_session


@bp.route("/session", methods=["POST"])
@cross_origin()
@jwt_required(optional=True)
@auto.doc()
def post_session():
    session_uuid = uuid.uuid4()
    session_created_timestamp = datetime.datetime.now(timezone.utc)
    user_uuid = None
    if current_user:
        user_uuid = current_user.user_uuid

    ip_address = get_ip_address(request)
    store_session(session_uuid, session_created_timestamp, user_uuid, ip_address)

    response = {"sessionId": session_uuid}

    return jsonify(response), 201
