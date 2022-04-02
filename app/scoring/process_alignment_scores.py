from app import db
from app.errors.errors import DatabaseError
from app.models import AlignmentScores, Conversations, Scores, Users
from scipy.stats import kendalltau


def create_alignment_scores(conversation_uuid, quiz_uuid, alignment_scores_uuid):
    """
    Calculate aligned scores based on user a and b quiz results and add to the alignment scores table.

    This is currently a dummy function.

    Parameters
    ==============
    conversation_uuid (UUID)
    quiz_uuid (UUID) - user b quiz uuid to compare scores with user a scores
    alignment_scores_uuid (UUID) - uuid created when post alignment endpoint is used
    """
    # TODO: Add logic to create aligned scores. Currently working with hard-coded dummy values.

    try:
        alignment_scores = AlignmentScores()
        alignment_scores.alignment_scores_uuid = alignment_scores_uuid
        alignment_scores.overall_similarity_score = calculate_overall_similarity_score(
            conversation_uuid, quiz_uuid
        )
        alignment_scores.top_match_percent = 90
        alignment_scores.top_match_value = "benevolence"
        alignment_scores.benevolence_alignment = 0.9
        alignment_scores.security_alignment = 0.85
        alignment_scores.self_direction_alignment = 0.8
        alignment_scores.power_alignment = 0.75
        alignment_scores.universalism_alignment = 0.7
        alignment_scores.achievement_alignment = 0.65
        alignment_scores.conformity_alignment = 0.6
        alignment_scores.tradition_alignment = 0.55
        alignment_scores.hedonism_alignment = 0.5
        alignment_scores.stimulation_alignment = 0.45

        db.session.add(alignment_scores)
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while adding scores to the alignment scores table."
        )


def calculate_overall_similarity_score(conversation_uuid, user_b_quiz_uuid):
    """
    Calculate the overall similarity score based on user b and user a's quiz results.

    Parameters
    ==========
    conversation_uuid (UUID)
    user_b_quiz_uuid (UUID)

    Returns
    ==========
    overall_similarity_score (float) - calculated using the Kendall Tau-B model, transformed (+1) and scaled (/2)
    """

    conversation, user_a_quiz_uuid = (
        db.session.query(Conversations, Users.quiz_uuid)
        .join(Users, Users.user_uuid == Conversations.sender_user_uuid)
        .filter(Conversations.conversation_uuid == conversation_uuid)
        .one_or_none()
    )

    user_a_scores_list = get_scores_list(user_a_quiz_uuid)
    user_b_scores_list = get_scores_list(user_b_quiz_uuid)

    overall_similarity_score = (
        kendalltau(user_a_scores_list, user_b_scores_list).correlation + 1
    ) / 2

    return overall_similarity_score


def get_scores_list(quiz_uuid):
    """
    Get a list of a user's quiz scores, ordered alphabetically by personal values.

    Parameters
    ==========
    quiz_uuid (UUID)

    Returns
    ==========
    scores_list - a list of floats
    """
    personal_values_categories = [
        "achievement",
        "benevolence",
        "conformity",
        "hedonism",
        "power",
        "security",
        "self_direction",
        "stimulation",
        "tradition",
        "universalism",
    ]

    user_scores = (
        db.session.query(Scores).filter(Scores.quiz_uuid == quiz_uuid).one_or_none()
    )

    user_scores = user_scores.__dict__

    scores_list = [user_scores[value] for value in personal_values_categories]

    return scores_list
