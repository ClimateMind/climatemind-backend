from email import message
from app.errors.errors import DatabaseError
from app.models import Conversations, UserBJourney, Users
import app.conversations.routes as con
from app import db
from app.user_b.analytics_logging import eventType, log_user_b_event


def build_single_conversation_response(conversation_uuid):
    """
    Deal with database interactions to provide response for get single conversation request.

    Parameters
    ==========
    conversation_uuid - (UUID) the unique id for the conversation

    Returns
    ==========
    JSON:
    - conversation uuid
    - user a's first name, user uuid, and the session uuid when they started the conversation
    - user b's name
    - conversation status
    - consent - if user b has consented to share info with user a
    - timestamp for when the conversation was created
    - alignment scores uuid (if consent=true)
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

    if conversation.user_b_share_consent:
        response["alignmentScoresId"] = (
            db.session.query(UserBJourney)
            .filter_by(conversation_uuid=conversation_uuid)
            .one()
        ).alignment_scores_uuid

    return response


def update_consent_choice(conversation_uuid, consent_choice, session_uuid):
    """
    Update user b's choice to share information with user a in the database.

    Parameters
    ==========
    conversation_uuid - (UUID) the unique id for the conversation
    consent_choice - (boolean) user b's consent choice
    session_uuid - (UUID) the unique id for user b's session

    Returns
    ==========
    JSON - success message or error
    """

    try:
        conversation, user_b_journey = (
            db.session.query(Conversations, UserBJourney)
            .join(
                UserBJourney,
                UserBJourney.conversation_uuid == Conversations.conversation_uuid,
            )
            .filter_by(conversation_uuid=conversation_uuid)
            .one_or_none()
        )
        conversation.user_b_share_consent = user_b_journey.consent = consent_choice

        if consent_choice:
            conversation.conversation_status = con.ConversationStatus.QuizCompleted
        else:
            conversation.conversation_status = con.ConversationStatus.Visited

    except:
        raise DatabaseError(
            message="Something went wrong while updating the consent choice in the conversations or user b journey tables."
        )

    log_user_b_event(conversation_uuid, session_uuid, eventType.CONSENT, consent_choice)

    return {"message": "Consent successfully updated."}
