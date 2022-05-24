from flask import current_app

from app.conversations.enums import ConversationStatus
from app import db
from app.errors.errors import DatabaseError
from app.models import Conversations, UserBJourney, Users, EffectChoice, SolutionChoice
import app.conversations.routes as con
from app import db
from app.user_b.analytics_logging import eventType, log_user_b_event
from app.network_x_tools.network_x_utils import network_x_utils
from app.alignment.utils import effect_details, solution_details


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

    if conversation.user_b_share_consent:
        alignment_scores_uuid = (
            db.session.query(UserBJourney)
            .filter_by(conversation_uuid=conversation_uuid)
            .one()
        ).alignment_scores_uuid
    else:
        alignment_scores_uuid = None

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
        "alignmentScoresId": alignment_scores_uuid,
    }

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
            conversation.conversation_status = ConversationStatus.QuizCompleted
        else:
            conversation.conversation_status = ConversationStatus.Visited

    except:
        raise DatabaseError(
            message="Something went wrong while updating the consent choice in the conversations or user b journey tables."
        )

    log_user_b_event(conversation_uuid, session_uuid, eventType.CONSENT, consent_choice)

    return {"message": "Consent successfully updated."}


def build_selected_topics_response(conversation_uuid):
    """Deal with database interactions to provide response for GET selected topics request.

    This includes effects and solutions. For the current model, there is always 1 selected effect
    and 2 selected solutions.

    Parameters
    ==========
    conversation_uuid - (UUID) the unique id for the conversation

    Returns
    ==========
    JSON:
    - the selected effects (always 1)
    - the selected solutions (always 2)

    """

    G = current_app.config["G"].copy()
    nx = network_x_utils()

    (user_b_journey, effect_choice, solution_choice) = (
        db.session.query(UserBJourney, EffectChoice, SolutionChoice)
        .join(
            EffectChoice,
            EffectChoice.effect_choice_uuid == UserBJourney.effect_choice_uuid,
        )
        .join(
            SolutionChoice,
            SolutionChoice.solution_choice_uuid == UserBJourney.solution_choice_uuid,
        )
        .filter(UserBJourney.conversation_uuid == conversation_uuid)
        .one_or_none()
    )

    climate_effect_iris = [effect_choice.effect_choice_1_iri]
    climate_effect_iris = [
        current_app.config.get("IRI_PREFIX") + iri for iri in climate_effect_iris
    ]
    climate_effects = effect_details(G, climate_effect_iris, nx)

    climate_solution_iris = [
        solution_choice.solution_choice_1_iri,
        solution_choice.solution_choice_2_iri,
    ]
    climate_solutions = solution_details(G, climate_solution_iris, nx)

    response = {
        "climateEffects": climate_effects,
        "climateSolutions": climate_solutions,
    }

    return response
