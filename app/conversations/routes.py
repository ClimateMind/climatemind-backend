from app.conversations import bp
from app import db
from app.models import Users
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from app.auth.routes import valid_name
from flask import request, jsonify, make_response
from flask_cors import cross_origin
import uuid


@bp.route("/create-conversation-invite", methods=["POST"])
@cross_origin()
@jwt_required()
def create_conversation_invite():
    r = request.get_json(force=True, silent=True)
    if not r:
        raise InvalidUsageError(
            message="Must provide a JSON body with the name of the invited user."
        )

    invited_name = r.get("invitedUserName")

    if not invited_name:
        raise InvalidUsageError(
            message="Must provide the name of the invited user."
        )

    valid_name(invited_name)

    identity = get_jwt_identity()
    user = db.session.query(Users).filter_by(user_uuid=identity).one_or_none()

    conversation_uuid = uuid.uuid4()

    response = {
        "message": "conversation created",
        "conversationId": conversation_uuid
    }

    return jsonify(response), 201


@bp.route("/get-conversations", methods=["GET"])
@cross_origin()
@jwt_required()
def get_conversations():
    identity = get_jwt_identity()
    user = db.session.query(Users).filter_by(user_uuid=identity).one_or_none()

    response = jsonify(
        {
            "invitedUserName": "Sean",
            "createdByUserId": uuid.uuid4(),
            "createdDateTime": "1995-22-12 07:45:34",
            "conversationId": uuid.uuid4()
        },
        {
            "invitedUserName": "Nick",
            "createdByUserId": uuid.uuid4(),
            "createdDateTime": "1995-22-12 08:20:21",
            "conversationId": uuid.uuid4()
        }
    )

    return response



