import datetime
from datetime import timezone
from enum import IntEnum
import uuid

from flask import jsonify, make_response, request
from flask_cors import cross_origin
from flask_jwt_extended import get_current_user, get_jwt_identity, jwt_required
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from app import db
from . import bp
from ..auth.utils import uuidType, validate_uuid, check_uuid_in_db
from ..errors.errors import DatabaseError, InvalidUsageError, UnauthorizedError
from ..models import Conversations, Scores, Sessions, Users


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

    :param invitedUserName: (str) Requires a name for the invited user

    :returns response: JSON with uuid4 as str
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
        return 2 < len(name) < 50

    if not invited_name or not valid_name(invited_name):
        raise InvalidUsageError(
            message="Must provide a name for the invited user that is between 2-50 characters long."
        )

    user = get_current_user()

    conversation_uuid = uuid.uuid4()

    conversation = Conversations(
        conversation_uuid=conversation_uuid,
        sender_user_uuid=user.user_uuid,
        sender_session_uuid=session_uuid,
        receiver_name=invited_name,
        conversation_status=ConversationStatus.Invited,
        conversation_created_timestamp=datetime.datetime.now(timezone.utc),
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

    :returns response: JSON conversations with the relevant names, UUIDs and creation dates.
    """
    session_uuid = request.headers.get("X-Session-Id")
    validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)
    user = get_current_user()

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


@bp.route("/shared-values", methods=["GET"])
@cross_origin()
@jwt_required()
def shared_values():
    """
    Users would like to see their shared values with other users & their similarity score.

    This endpoint returns this data.

    TODO: Integrate shared values
    """
    session_uuid = request.headers.get("X-Session-Id")
    validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)
    user = get_current_user()

    r = request.get_json(force=True, silent=True)
    if not r:
        raise InvalidUsageError(
            message="Must provide a JSON body with the Conversation ID."
        )

    conversation_id = r.get("conversationId")
    conversation = (
        db.session.query(Conversations)
        .filter_by(conversation_id=conversation_id)
        .one_or_none()
    )

    if not conversation:
        raise InvalidUsageError(message="conversationId is Invalid.")

    sender_uuid, sender_scores = Scores.get_scores_list(
        conversation.sender_session_uuid
    )
    receiver_uuid, receiver_scores = Scores.get_scores_list(
        conversation.receiver_session_uuid
    )

    # User needs to be associated with a conversation to access it
    if sender_uuid != user.user_uuid and receiver_uuid != user.user_uuid:
        raise DatabaseError(message="conversationId is Invalid.")

    if not sender_scores or not receiver_scores:
        raise DatabaseError(message="Conversation is missing required data.")

    similarity_score = (kendalltau(a, b).correlation + 1) / 2

    return jsonify({"similarityScore": similarity_score}), 200
