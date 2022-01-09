from app import db
from app.errors.errors import DatabaseError
from app.models import AlignmentScores


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
        alignment_scores.overall_similarity_score = 0.7
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
