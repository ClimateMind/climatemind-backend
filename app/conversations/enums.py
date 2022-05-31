from enum import IntEnum


class ConversationStatus(IntEnum):
    """
    Conversation status is used to identify where a user is
    in their journey to communicate with other users they invite.

    This enum should not be modified unless the frontend is involved in the change.
    """

    Invited = 0
    Visited = 1
    QuizCompleted = 2
    ConversationCompleted = 3


class ConversationState(IntEnum):
    """
    State which identifies how far along user A is in seeing the conversation results with user B.
    """

    InvitedUserB = 0
    UserBDone = 1
    AlignButtonClicked = 2
    TalkButtonClicked = 3
    DoneButtonClicked = 4
    ConversationRated = 5
