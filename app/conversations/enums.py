from enum import IntEnum, Enum


class ConversationStatus(IntEnum):
    """
    Conversation status is used to identify where a user is
    in their journey to communicate with other users they invite.

    # FIXME: deprecated
    This enum should not be modified unless the frontend is involved in the change.
    """

    Invited = 0
    Visited = 1
    QuizCompleted = 2
    ConversationCompleted = 3


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


class ConversationButtonMapState(IntEnum):
    aligned = ConversationState.AlignButtonClicked
    topics = ConversationState.TopicsButtonClicked
    talked = ConversationState.TalkedButtonClicked


class ConversationUserARating(IntEnum):
    AWFUL = 1
    BAD = 2
    MEDIOCRE = 3
    GOOD = 4
    EXCELLENT = 5
