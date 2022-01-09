from app import db
from app.errors.errors import DatabaseError
from app.models import AlignmentFeed


def create_alignment_feed(conversation_uuid, quiz_uuid, alignment_feed_uuid):
    """
    Calculate aligned feed based on user a and b quiz results and add to the alignment feed table.

    This is currently a dummy function.

    Parameters
    ==============
    conversation_uuid (UUID)
    quiz_uuid (UUID) - user b quiz uuid to compare scores with user a scores
    alignment_feed_uuid (UUID) - uuid created when post alignment endpoint is used
    """
    # TODO: Add logic to create aligned feed. Currently working with hard-coded dummy values.

    try:
        alignment_feed = AlignmentFeed()
        alignment_feed.alignment_feed_uuid = alignment_feed_uuid
        alignment_feed.aligned_effect_1_iri = "R9JAWzfiZ9haeNhHiCpTWkr"
        alignment_feed.aligned_effect_2_iri = "R8JoXNnKTYqERwU7fblKTWB"
        alignment_feed.aligned_effect_3_iri = "RB7k7p2iQQgKdQrkRP2MZWM"
        alignment_feed.aligned_solution_1_iri = "RBeBCvukdLNSe5AtnlJpQ1k"
        alignment_feed.aligned_solution_2_iri = "R9SuseoJG7H6QeUEvZwLciQ"
        alignment_feed.aligned_solution_3_iri = "R9R6552i4fn3XHKpoV8QTOx"
        alignment_feed.aligned_solution_4_iri = "RDSZw453Ge76hYTvYEsaAwU"
        alignment_feed.aligned_solution_5_iri = "RDanTqMAQyQ4nGzlrt0j7Bm"
        alignment_feed.aligned_solution_6_iri = "RItKzuJSSFw9hXydUSVEJX"
        alignment_feed.aligned_solution_7_iri = "RBCQdAOKui38ytAIKZlpPN6"
        db.session.add(alignment_feed)
        db.session.commit
    except:
        raise DatabaseError(
            message="An error occurred while adding the alignment feed to the database."
        )
