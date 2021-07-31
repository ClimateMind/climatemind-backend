from app.session import bp
from app.models import Sessions
from app.session.session_helpers import process_ip_address, store_session
from flask import jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user
import datetime
from datetime import timezone

from app import auto

import uuid


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

    store_session(session_uuid, session_created_timestamp, user_uuid)
    process_ip_address(request, session_uuid)

    response = {"sessionId": session_uuid}

    return jsonify(response), 201
