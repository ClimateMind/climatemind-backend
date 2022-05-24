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
