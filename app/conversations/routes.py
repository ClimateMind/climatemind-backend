import datetime
import uuid
from datetime import timezone

from flask import request, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc

from app import db
from app.common.schemas import validate_schema_field
from app.common.uuid import (
    validate_uuid,
    uuidType,
    check_uuid_in_db,
)
from app.conversations import bp
from app.conversations.enums import ConversationState
from app.conversations.schemas import ConversationEditSchema
from app.conversations.utils import (
    build_single_conversation_response,
    update_consent_choice,
    build_selected_topics_response,
)
from app.errors.errors import (
    DatabaseError,
    InvalidUsageError,
    NotInDatabaseError,
    ForbiddenError,
)
from app.models import Users, Conversations
from app.sendgrid.utils import send_user_b_shared_email


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
        state=ConversationState.UserBInvited,
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
        .filter_by(is_marked_deleted=False)
        .order_by(desc(Conversations.conversation_created_timestamp))
        .all()
    )

    results = []
    for conversation in conversations:
        results.append(
            # FIXME: just a hotfix, refactor
            build_single_conversation_response(conversation.conversation_uuid)
        )

    response = {"conversations": results}

    return jsonify(response), 200


@bp.route("/conversation/<conversation_uuid>", methods=["GET"])
@cross_origin()
def get_conversation(conversation_uuid):
    """
    Validates and returns a single conversation.

    Parameters
    ==========
    conversation_uuid - (UUID) the unique id for the conversation

    Returns
    ==========
    JSON:
    - conversation uuid
    - user a's first name, user uuid, and the session uuid when they started the conversation
    - user b's name
    - conversation state
    - consent - if user b has consented to share info with user a
    - timestamp for when the conversation was created
    """

    conversation_uuid = validate_uuid(conversation_uuid, uuidType.CONVERSATION)
    check_uuid_in_db(conversation_uuid, uuidType.CONVERSATION)
    response = build_single_conversation_response(conversation_uuid)

    return jsonify(response), 200


@bp.route("/conversation/<conversation_uuid>/consent", methods=["POST"])
@cross_origin()
def post_consent(conversation_uuid):
    """
    Updates user b's choice to share information with user a in the database.
    Sends a confirmation email to user a that user b has shared.

    Parameters
    ==========
    conversation_uuid - (UUID) the unique id for the conversation

    Returns
    ==========
    JSON - success message or error
    """

    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    conversation_uuid = validate_uuid(conversation_uuid, uuidType.CONVERSATION)
    check_uuid_in_db(conversation_uuid, uuidType.CONVERSATION)

    r = request.get_json(force=True, silent=True)
    consent_choice = r.get("consent")
    if not isinstance(consent_choice, bool):
        raise InvalidUsageError(message="Consent must be a boolean.")

    response = update_consent_choice(conversation_uuid, consent_choice, session_uuid)

    send_user_b_shared_email(conversation_uuid)

    return jsonify(response), 201


@bp.route("/conversation/<conversation_uuid>", methods=["PUT"])
@cross_origin()
@jwt_required()
def edit_conversation(conversation_uuid):
    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    schema = ConversationEditSchema()
    uuid_field_name = "conversationId"
    validate_schema_field(schema, uuid_field_name, conversation_uuid)

    conversation = Conversations.query.filter_by(
        conversation_uuid=conversation_uuid,
        is_marked_deleted=False,
    ).first()
    identity = get_jwt_identity()

    if not conversation:
        raise NotInDatabaseError(message="Conversation not found")
    elif conversation.sender_user_uuid != identity:
        raise ForbiddenError(message="User doesn't have access to the conversation")
    else:
        json_data = request.get_json(force=True, silent=True)
        json_data[uuid_field_name] = conversation_uuid

        try:
            conversation = schema.load(json_data, instance=conversation, partial=True)
            db.session.commit()
            return schema.jsonify(conversation)
        except SQLAlchemyError:
            return DatabaseError(message="Couldn't edit conversation")


@bp.route("/conversation/<conversation_uuid>", methods=["DELETE"])
@cross_origin()
@jwt_required()
def delete_conversation(conversation_uuid):
    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    conversation_uuid = validate_uuid(conversation_uuid, uuidType.CONVERSATION)

    conversation = Conversations.query.filter_by(
        conversation_uuid=conversation_uuid,
        is_marked_deleted=False,
    ).first()
    identity = get_jwt_identity()

    if not conversation:
        raise NotInDatabaseError(message="Conversation not found")
    elif conversation.sender_user_uuid != identity:
        raise ForbiddenError(message="User doesn't have access to the conversation")
    else:
        try:
            conversation.is_marked_deleted = True
            db.session.commit()
            response = {
                "message": "Conversation has removed successfully.",
                "conversationId": conversation_uuid,
            }
            return jsonify(response), 204
        except SQLAlchemyError:
            return DatabaseError(message="Couldn't edit conversation")


@bp.route("/conversation/<conversation_uuid>/topics", methods=["GET"])
@cross_origin()
def get_topics(conversation_uuid):
    """Get the topics selected by user B from their alignment with user A.

    Includes both effects and solutions in the response body. Based on the current design, there is
    always one effect and two solutions.

    Also includes session uuid validation and format checking.

    Parameters
    ===========
    conversation_uuid - (UUID) the unique id for the conversation

    Returns
    ===========
    A dict of user B's selected effects and solutions.

    """
    session_uuid = request.headers.get("X-Session-Id")
    validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    response = build_selected_topics_response(conversation_uuid)

    return jsonify(response), 200
