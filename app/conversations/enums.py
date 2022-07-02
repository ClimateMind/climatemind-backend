from enum import IntEnum


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


class ConversationUserARating(IntEnum):
    AWFUL = 1
    BAD = 2
    MEDIOCRE = 3
    GOOD = 4
    EXCELLENT = 5
