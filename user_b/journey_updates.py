from app import db
from app.errors.errors import DatabaseError
from app.models import UserBJourney
from enum import Enum


def start_user_b_journey(conversation_uuid):
    """
    Save the conversation uuid to the user b journey table to centralise most up-to-date information
    for user b.
    """
    if not UserBJourney.query.filter_by(
        conversation_uuid=conversation_uuid
    ).one_or_none():
        try:
            user_b = UserBJourney()
            user_b.conversation_uuid = conversation_uuid
            db.session.add(user_b)
            db.session.commit()
        except:
            raise DatabaseError(
                message="An error occurred while saving data to the user b journey table."
            )


def update_user_b_journey(conversation_uuid, **kwargs):
    """
    Update information in the user b journey table when actions are done, or redone during the user b journey
    through the app.

    Parameters
    =================
    conversation_uuid (UUID)
    userBInfo (Enum)
    new_value (UUID or boolean) - consent is boolean, all other values are UUIDs
    """
    user_b = UserBJourney.query.filter_by(
        conversation_uuid=conversation_uuid
    ).one_or_none()
    try:
        for key, value in kwargs.items():
            if key == "quiz_uuid":
                user_b.quiz_uuid = value
            elif key == "alignment_scores_uuid":
                user_b.alignment_scores_uuid = value
            elif key == "alignment_feed_uuid":
                user_b.alignment_feed_uuid = value
            elif key == "effect_choice_uuid":
                user_b.effect_choice_uuid = value
            elif key == "solution_choice_uuid":
                user_b.solution_choice_uuid = value
            elif key == "consent":
                user_b.consent = value
            db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while updating an item in the user b journey table."
        )
