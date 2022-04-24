from app import db
from app.errors.errors import DatabaseError
from app.models import AlignmentFeed, Scores, Users, Conversations
from app.alignment.utils import map_associated_personal_values
from app.scoring.build_localised_acyclic_graph import get_node_id
from app.scoring.process_alignment_scores import *
from flask import current_app


def create_alignment_feed(conversation_uuid, quiz_uuid, alignment_feed_uuid, alignment_scores_uuid):
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

    aligned_effect_iris = get_aligned_effects(conversation_uuid, quiz_uuid, alignment_scores_uuid)

    try:
        alignment_feed = AlignmentFeed()
        alignment_feed.alignment_feed_uuid = alignment_feed_uuid
        alignment_feed.aligned_effect_1_iri = aligned_effect_iris[0]
        alignment_feed.aligned_effect_2_iri = aligned_effect_iris[1]
        alignment_feed.aligned_effect_3_iri = aligned_effect_iris[2]
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


def get_aligned_effects(conversation_uuid, quiz_uuid, alignment_scores_uuid):
    """
    Creates a list of IRIs for impacts/effects from the ontology that are positively associated with the top aligned personal
    value between users A and B calculated based on comparison of their quiz results.

    Currently set to return 3 effects.
    """
    number_of_effects_to_return = 3
    aligned_effect_iris = []

    user_a_value_scores = None
    user_b_value_scores = None
    number_of_personal_values_to_check = 4

    # def backfire effect by top values
    
    G = current_app.config["G"].copy()

    aligned_scores = db.session.query(AlignmentScores).filter(AlignmentScores.alignment_scores_uuid == alignment_scores_uuid).one_or_none()
    top_aligned_value = aligned_scores.top_match_value

    for node in G.nodes:
        current_node = G.nodes[node]

        if "effect" in current_node["all classes"]:
            associated_personal_values = map_associated_personal_values(current_node["personal_values_10"])
            
            if top_aligned_value in associated_personal_values:
                aligned_effect_iris.append(get_node_id(current_node))
                    
                if len(aligned_effect_iris) >= number_of_effects_to_return:
                    break                    

    return aligned_effect_iris

