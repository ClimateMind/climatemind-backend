from app.conversations import bp
from app import db
from app.auth.utils import uuidType, validate_uuid
from app.models import Users, Conversation, Sessions
from app.errors.errors import DatabaseError
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask import request, jsonify, make_response
from flask_cors import cross_origin
import datetime
from datetime import timezone
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from enum import IntEnum
import uuid


class ConversationStatus(IntEnum):
    """
    Conversation status is used to identify where a user is
    in their journey to communicate with other users they invite.

    This enum should not be modified unless the frontend is involved in the change.
    """

    Invited = 1
    Visited = 2
    QuizCompleted = 3
    ConversationCompleted = 4


@bp.route("/create-conversation-invite", methods=["POST"])
@cross_origin()
@jwt_required()
def create_conversation_invite():
    """
    Users can invite friends to conversations. These conversations are given a unique
    UUID which is used to create a URL invite for their friend. This endpoint creates
    a new conversation in the database.

    Parameters
    ==========
    invitedUserName - (str) Requires a name for the invited user

    Returns
    ==========
    The unique conversation UUID and a datetime stamp
    """
    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    r = request.get_json(force=True, silent=True)
    if not r:
        raise InvalidUsageError(
            message="Must provide a JSON body with the name of the invited user."
        )

    invited_name = r.get("invitedUserName")

    def valid_name(name):
        return 2 < len(name) < 50

    if not invited_name or not valid_name(invited_name):
        raise InvalidUsageError(message="Must provide the name of the invited user.")

    identity = get_jwt_identity()
    user = db.session.query(Users).filter_by(user_uuid=identity).one_or_none()

    if not user:
        raise DatabaseError(message="No user found for the provided JWT token.")

    conversation_uuid = uuid.uuid4()

    conversation = Conversation(
        conversation_uuid=conversation_uuid,
        sender_user_uuid=user.user_uuid,
        sender_session_uuid=session_uuid,
        receiver_name=invited_name,
        conversation_status=ConversationStatus.Invited,
        conversation_create_time=datetime.datetime.now(timezone.utc),
    )

    try:
        db.session.add(conversation)
        db.session.commit()

    except SQLAlchemyError:
        raise DatabaseError(message="Failed to add conversation to database")

    response = {"message": "conversation created", "conversationId": conversation_uuid}

    return jsonify(response), 201


@bp.route("/get-conversations", methods=["GET"])
@cross_origin()
@jwt_required()
def get_conversations():
    """
    Users would like to be able to see a list of all of their pending/current conversations
    as well as the status. This endpoints returns this data for their feed.

    Parameters
    ===========
    No Parameters. Only the JWT Token is required.

    Returns
    ===========
    A list of the user's conversations with the relevant names, UUIDs and creation dates.
    """
    session_uuid = request.headers.get("X-Session-Id")
    validate_uuid(session_uuid, uuidType.SESSION)
    identity = get_jwt_identity()
    user = db.session.query(Users).filter_by(user_uuid=identity).one_or_none()

    if not user:
        raise DatabaseError(message="No user found for the provided JWT token")

    conversations = (
        db.session.query(Conversation).filter_by(sender_user_uuid=user.user_uuid).all()
    )

    results = []
    for conversation in conversations:
        results.append(
            {
                "invitedUserName": conversation.receiver_name,
                "createdByUserId": user.user_uuid,
                "createdDateTime": conversation.conversation_create_time,
                "conversationId": conversation.conversation_uuid,
                "conversationStatus": conversation.conversation_status,
            }
        )

    response = {"conversations": results}

    return jsonify(response), 201
