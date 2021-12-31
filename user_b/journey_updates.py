from app import db
from app.errors.errors import DatabaseError
from app.models import UserBJourney


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
