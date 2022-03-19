from enum import Enum
import uuid
from app import db
from app.errors.errors import DatabaseError
from app.models import UserBAnalyticsData
from datetime import datetime, timezone
from enum import Enum


class eventType(Enum):
    """
    Event types to be used for analytics logging.

    LINK - the unique link for user b has been used
    SOLUTION - user b has made a choice for a shared solution to discuss with user a
    EFFECT - user b has made a choice for a shared effect to discuss with user a
    CONSENT - user b has updated whether they consent to share information on their choices with user a
    QUIZ - user b has completed the quiz
    LMEFFECT - user b has clicked on a shared impact card to learn more
    LMSOLUTION - user b has clicked on a shared solution card to learn more
    """

    LINK = 1
    SOLUTION = 2
    EFFECT = 3
    CONSENT = 4
    QUIZ = 5
    LMEFFECT = 6
    LMSOLUTION = 7


def log_user_b_event(conversation_uuid, session_uuid, event_type, event_value):
    """
    Log an event in the user b analytics data table.
    """
    try:
        event_to_add = UserBAnalyticsData()
        event_to_add.event_log_uuid = uuid.uuid4()
        event_to_add.conversation_uuid = conversation_uuid
        event_to_add.event_value = event_value
        event_to_add.event_timestamp = datetime.now(timezone.utc)
        event_to_add.session_uuid = session_uuid

        if event_type.name == "LINK":
            event_to_add.event_type = "link clicked"
            event_to_add.event_value_type = "boolean"
        elif event_type.name == "CONSENT":
            event_to_add.event_type = "consent updated"
            event_to_add.event_value_type = "boolean"
        elif event_type.name == "EFFECT":
            event_to_add.event_type = "effect choice"
            event_to_add.event_value_type = "UUID"
        elif event_type.name == "SOLUTION":
            event_to_add.event_type = "solution choice"
            event_to_add.event_value_type = "UUID"
        elif event_type.name == "QUIZ":
            event_to_add.event_type = "quiz completed"
            event_to_add.event_value_type = "UUID"
        elif event_type.name == "LMEFFECT":
            event_to_add.event_type = "learn more - impact"
            event_to_add.event_value_type = "IRI"
        elif event_type.name == "LMSOLUTION":
            event_to_add.event_type = "learn more - solution"
            event_to_add.event_value_type = "IRI"

        db.session.add(event_to_add)
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while logging a user b analytics event."
        )
