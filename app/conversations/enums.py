import typing
from enum import IntEnum

from app.user_b.analytics_logging import eventType


class ConversationState(IntEnum):
    """
    State which identifies how far along user A is in seeing
    the conversation results with user B.
    """

    UserBInvited = 0
    UserBConsented = 1
    AlignButtonClicked = 2
    TopicsButtonClicked = 3
    TalkedButtonClicked = 4
    RatingDone = 5

    def get_analytics_event_type(self) -> typing.Optional[eventType]:
        conversation_state_to_analytics_event_type_mapping = {
            self.AlignButtonClicked: eventType.UA_ALIGN_CLICK,
            self.TopicsButtonClicked: eventType.UA_TOPICS_CLICK,
            self.TalkedButtonClicked: eventType.UA_TALKED_CLICK,
            self.RatingDone: eventType.UA_RATING_DONE,
        }
        return conversation_state_to_analytics_event_type_mapping.get(self)


class ConversationUserARating(IntEnum):
    AWFUL = 1
    BAD = 2
    MEDIOCRE = 3
    GOOD = 4
    EXCELLENT = 5
