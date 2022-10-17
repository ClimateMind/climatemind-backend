from enum import Enum
import uuid
from app import db
from app.errors.errors import DatabaseError
from app.models import UserBAnalyticsData
from datetime import datetime, timezone
from enum import Enum


class eventType(Enum):
    """
    TODO: rename
    Event types to be used for analytics logging.

    LINK - the unique link for user b has been used
    SOLUTION - user b has made a choice for a shared solution to discuss with user a
    EFFECT - user b has made a choice for a shared effect to discuss with user a
    CONSENT - user b has updated whether they consent to share information on their choices with user a
    QUIZ - user b has completed the quiz
    LMEFFECT - user b has clicked on a shared impact card to learn more
    LMSOLUTION - user b has clicked on a shared solution card to learn more

    UA_ALIGN_CLICK - user a clicked align button
    UA_TOPICS_CLICK - user a clicked topics button
    UA_TALKED_CLICK - user a clicked talked button
    UA_RATING_DONE = rating done by user a
    """

    LINK = "link clicked"
    SOLUTION = "solution choice"
    EFFECT = "effect choice"
    CONSENT = "consent updated"
    QUIZ = "quiz completed"
    LMEFFECT = "learn more - impact"
    LMSOLUTION = "learn more - solution"

    UA_ALIGN_CLICK = "align button clicked"
    UA_TOPICS_CLICK = "topics button clicked"
    UA_TALKED_CLICK = "talked button clicked"
    UA_RATING_DONE = "rating done"

    def get_event_value_type(self):
        event_to_event_type_mapping = {
            self.LINK: EventValueTypeEnum.BOOLEAN,
            self.CONSENT: EventValueTypeEnum.BOOLEAN,
            self.EFFECT: EventValueTypeEnum.UUID,
            self.SOLUTION: EventValueTypeEnum.UUID,
            self.QUIZ: EventValueTypeEnum.UUID,
            self.LMEFFECT: EventValueTypeEnum.IRI,
            self.LMSOLUTION: EventValueTypeEnum.IRI,
            self.UA_ALIGN_CLICK: EventValueTypeEnum.BOOLEAN,
            self.UA_TOPICS_CLICK: EventValueTypeEnum.BOOLEAN,
            self.UA_TALKED_CLICK: EventValueTypeEnum.BOOLEAN,
            self.UA_RATING_DONE: EventValueTypeEnum.BOOLEAN,
        }
        return event_to_event_type_mapping[self]


class EventValueTypeEnum(Enum):
    BOOLEAN = "boolean"
    UUID = "UUID"
    IRI = "IRI"


def log_user_b_event(conversation_uuid, session_uuid, event_type, event_value):
    """
    TODO: rename
    Log an event in the user b analytics data table.
    """
    try:
        event_to_add = UserBAnalyticsData()
        event_to_add.event_log_uuid = uuid.uuid4()
        event_to_add.conversation_uuid = conversation_uuid
        event_to_add.event_value = event_value
        event_to_add.event_timestamp = datetime.now(timezone.utc)
        event_to_add.session_uuid = session_uuid
        event_to_add.event_type = event_type.value
        event_to_add.event_value_type = event_type.get_event_value_type().value

        db.session.add(event_to_add)
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while logging a user b analytics event."
        )
