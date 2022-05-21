from app import db
from app.common.math_utils import as_percent
from app.errors.errors import DatabaseError
from app.personal_values.enums import PersonalValue
from app.models import AlignmentScores, Conversations, Scores, Users
from scipy.stats import kendalltau

from app.scoring.process_scores import get_scores_list, get_scores_map


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
            db.session.query(Scores).filter(Scores.quiz_uuid == quiz_uuid).one()
        )
        userA_score_map = get_scores_map(userA_scores)
        userB_score_map = get_scores_map(userB_scores)
        userA_rank_map = get_rank_map(userA_score_map)
        userB_rank_map = get_rank_map(userB_score_map)
        alignment_map = get_alignment_map(userA_rank_map, userB_rank_map)
        (max_name, max_value) = get_max(alignment_map)

        alignment_scores = AlignmentScores()
        alignment_scores.alignment_scores_uuid = alignment_scores_uuid
        for personal_value_key in PersonalValue.get_all_keys():
            setattr(
                alignment_scores,
                personal_value_key + "_alignment",
                alignment_map[personal_value_key],
            )
        alignment_scores.top_match_value = max_name
        alignment_scores.top_match_percent = as_percent(max_value)
        alignment_scores.overall_similarity_score = calculate_overall_similarity_score(
            conversation_uuid, quiz_uuid
        )

        db.session.add(alignment_scores)
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while adding scores to the alignment scores table."
        )


def get_rank_map(score_map):
    """Derive a rank map from a score map for a user's scores."""
    sorted_values = sorted(score_map.values(), reverse=True)
    return {name: sorted_values.index(score) + 1 for (name, score) in score_map.items()}


def get_alignment_map(rank_map1, rank_map2):
    """Derive an alignment map from two users' rank maps."""
    return {
        name: calculate_match(rank_map1[name], rank_map2[name])
        for name in rank_map1.keys()
    }


def get_sorted_alignment_map(alignment_map):
    """Sort the alignment scores map for two users from highest to lowest"""
    return sorted(alignment_map.items(), key=lambda x: -x[1])


def get_max(alignment_map):
    """Find the max alignment score with its personal value name."""
    return sorted(alignment_map.items(), key=lambda pair: -pair[1])[0]


def calculate_match(rank1, rank2):
    """Calculate the similarity score between two users' score ranks for a particular personal value.

    The formula features the following mathematical behaviors:
    - a penalty for how different a personal value ranks for user a compared to user b
    - a penalty for how unimportant a personal value is for both user a and user b

    For more detail, see
    https://docs.google.com/document/d/1cqmBvNd8sWV1d6EvmTLgp6DlR3h1RVgW7pNDGgmV_k4.

    Parameters:
    rank1(int): the rank of user A's score for a particular personal value within her quiz scores
    rank2(int): the rank of user B's score for a particular personal value within her quiz scores

    Return:
    float: the calculated similarity score
    """
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
