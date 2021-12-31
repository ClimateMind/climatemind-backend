from app.conversations import bp
from app import db
from app.conversations.utils import build_single_conversation_response
from app.auth.utils import validate_uuid, check_uuid_in_db, uuidType
from app.models import Users, Conversations, Sessions
from app.errors.errors import DatabaseError, InvalidUsageError
from user_b.analytics_logging import log_user_b_event, eventType
from user_b.journey_updates import start_user_b_journey
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

    Invited = 0
    Visited = 1
    QuizCompleted = 2
    ConversationCompleted = 3


@bp.route("/conversation", methods=["POST"])
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
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    r = request.get_json(force=True, silent=True)
    if not r:
        raise InvalidUsageError(
            message="Must provide a JSON body with the name of the invited user."
        )

    invited_name = r.get("invitedUserName")

    def valid_name(name):
        return 0 < len(name) <= 20

    if not invited_name or not valid_name(invited_name):
        raise InvalidUsageError(
            message="Must provide a name that is up to 20 characters long."
        )

    identity = get_jwt_identity()
    user = db.session.query(Users).filter_by(user_uuid=identity).one_or_none()

    # TODO - WE NEED TO DECIDE WHETHER TO DELETE THIS. THE APP WILL NEVER REACH THIS ERROR AS JWT IS
    # REQUIRED AND THE JWT STANDARD ERRORS WILL KICK IN FIRST.
    # if not user:
    #    raise DatabaseError(message="No user found for the provided JWT token.")

    conversation_uuid = uuid.uuid4()

    conversation = Conversations(
        conversation_uuid=conversation_uuid,
        sender_user_uuid=user.user_uuid,
        sender_session_uuid=session_uuid,
        receiver_name=invited_name,
        conversation_status=ConversationStatus.Invited,
        conversation_created_timestamp=datetime.datetime.now(timezone.utc),
        user_b_share_consent=False,
    )

    try:
        db.session.add(conversation)
        db.session.commit()
    except SQLAlchemyError:
        raise DatabaseError(message="Failed to add conversation to database")

    response = {"message": "conversation created", "conversationId": conversation_uuid}

    return jsonify(response), 201


@bp.route("/conversations", methods=["GET"])
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
    check_uuid_in_db(session_uuid, uuidType.SESSION)
    identity = get_jwt_identity()
    user = db.session.query(Users).filter_by(user_uuid=identity).one_or_none()

    conversations = (
        db.session.query(Conversations)
        .filter_by(sender_user_uuid=user.user_uuid)
        .order_by(Conversations.conversation_created_timestamp)
        .all()
    )

    results = []
    for conversation in conversations:
        results.append(
            {
                "invitedUserName": conversation.receiver_name,
                "createdByUserId": user.user_uuid,
                "createdDateTime": conversation.conversation_created_timestamp,
                "conversationId": conversation.conversation_uuid,
                "conversationStatus": conversation.conversation_status,
            }
        )

    response = {"conversations": results}

    return jsonify(response), 200


@bp.route("/conversation/<conversation_uuid>", methods=["GET"])
@cross_origin()
def get_conversation(conversation_uuid):
    """
    Get a single conversation.
    """
    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    validate_uuid(conversation_uuid, uuidType.CONVERSATION)
    check_uuid_in_db(conversation_uuid, uuidType.CONVERSATION)
    response = build_single_conversation_response(conversation_uuid)

    start_user_b_journey(conversation_uuid)
    log_user_b_event(conversation_uuid, session_uuid, eventType.LINK, 1)

    return jsonify(response), 200
