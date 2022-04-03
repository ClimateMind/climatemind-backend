from app import db
from app.errors.errors import DatabaseError
from app.personal_values.utils import get_value_descriptions_map
from app.models import AlignmentScores, Conversations, Scores, Users
from scipy.stats import kendalltau

def create_alignment_scores(conversation_uuid, quiz_uuid, alignment_scores_uuid):
    """
    Calculate aligned scores based on user a and b quiz results and add to the alignment scores table.

    Parameters
    ==============
    conversation_uuid (UUID)
    quiz_uuid (UUID) - user b quiz uuid to compare scores with user a scores
    alignment_scores_uuid (UUID) - uuid created when post alignment endpoint is used
    """
    try:
        userA_scores = (
            db.session.query(Scores)
            .join(Users, Users.quiz_uuid == Scores.quiz_uuid)
            .join(Conversations, Conversations.sender_user_uuid == Users.user_uuid)
            .filter(Conversations.conversation_uuid == conversation_uuid)
            .one()
        )
        userB_scores = (
            db.session.query(Scores)
            .filter(Scores.quiz_uuid == quiz_uuid)
            .one()
        )
        value_names = get_value_descriptions_map().keys()
        userA_rank_map = get_rank_map(userA_scores, value_names)
        userB_rank_map = get_rank_map(userB_scores, value_names)
        alignment_map = {name: calculate_match(userA_rank_map[name], userB_rank_map[name]) for name in value_names}
        (max_name, max_value) = sorted(alignment_map.items(), key=lambda pair:-pair[1])[0]

        alignment_scores = AlignmentScores()
        alignment_scores.alignment_scores_uuid = alignment_scores_uuid
        for name in value_names:
            setattr(alignment_scores, name + '_alignment', alignment_map[name])
        alignment_scores.top_match_value = max_name
        alignment_scores.top_match_percent = max_value  # TODO: convert to percentage?
        alignment_scores.overall_similarity_score = calculate_overall_similarity_score(
            conversation_uuid, quiz_uuid
        )

        db.session.add(alignment_scores)
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while adding scores to the alignment scores table."
        )

def get_rank_map(scores, value_names):
    score_map = {name: getattr(scores, name) for name in value_names}
    sorted_values = sorted(score_map.values(), reverse=True)
    return {name: sorted_values.index(score) + 1 for (name, score) in score_map.items()}

def calculate_match(rank1, rank2):
    (r1, r2) = (float(rank1), float(rank2))
    return (
        1.0
        - (0.00849 * ((r1 - r2) ** 2.0))
        - (0.00802 * abs(r1 - r2))
        - (0.0005 * (((r1 + r2) / 2.0) ** 2.0))
        - (0.0501 * ((r1 + r2) / 2.0))
        + 0.0506
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
