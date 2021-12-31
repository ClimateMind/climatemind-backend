from app.models import Conversations, Users
from app import db


def build_single_conversation_response(conversation_uuid):
    """
    Deal with database interactions to provide response for get single conversation request.
    """
    conversation = (
        db.session.query(Conversations)
        .filter_by(conversation_uuid=conversation_uuid)
        .one_or_none()
    )
    user_A_name = (
        db.session.query(Users)
        .filter_by(user_uuid=conversation.sender_user_uuid)
        .one_or_none()
    ).first_name

    response = {
        "conversationId": conversation.conversation_uuid,
        "userA": {
            "name": user_A_name,
            "id": conversation.sender_user_uuid,
            "sessionId": conversation.sender_session_uuid,
        },
        "userB": {
            "name": conversation.receiver_name,
        },
        "conversationStatus": conversation.conversation_status,
        "consent": conversation.user_b_share_consent,
        "conversationTimestamp": conversation.conversation_created_timestamp,
    }

    return response
