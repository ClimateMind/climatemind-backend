from app import db
from app.errors.errors import DatabaseError
from app.models import AlignmentFeed, Scores, Users, Conversations
from app.alignment.utils import *
from app.scoring.build_localised_acyclic_graph import get_node_id
from app.scoring.process_alignment_scores import *
from flask import current_app


def create_alignment_feed(
    conversation_uuid, quiz_uuid, alignment_feed_uuid, alignment_scores_uuid
):
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

    aligned_effects = list(get_aligned_effects(alignment_scores_uuid).keys())

    try:
        alignment_feed = AlignmentFeed()
        alignment_feed.alignment_feed_uuid = alignment_feed_uuid
        alignment_feed.aligned_effect_1_iri = aligned_effects[0]
        alignment_feed.aligned_effect_2_iri = aligned_effects[1]
        alignment_feed.aligned_effect_3_iri = aligned_effects[2]
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


def get_aligned_effects(alignment_scores_uuid):
    """
    Creates a sorted dictionary of IRIs and dot products for impacts/effects from the ontology that are positively associated with the top aligned personal
    value for users A and B (calculated based on comparison of their quiz results).

    Params
    ==========
    alignment_scores_uuid (UUID) - the uuid for the aligned scores for users a and b

    Returns
    ==========
    aligned_effects - a sorted dictionary of effects positively associated with user a and b's top shared value
    """
    aligned_effects = dict()

    G = current_app.config["G"].copy()

    aligned_scores = (
        db.session.query(AlignmentScores)
        .filter(AlignmentScores.alignment_scores_uuid == alignment_scores_uuid)
        .one_or_none()
    )
    top_aligned_value = aligned_scores.top_match_value
    aligned_scores = get_aligned_scores(aligned_scores)
    aligned_scores_vector = vectorise(aligned_scores)
    transformed_aligned_scores = transform_aligned_scores(aligned_scores_vector)

    for node in G.nodes:
        current_node = G.nodes[node]

        if "risk" in current_node["all classes"] and "test ontology" in current_node["all classes"] and not all([value == None for value in current_node["personal_values_10"]]):
            associated_personal_values = map_associated_personal_values(
                current_node["personal_values_10"]
            )

            if top_aligned_value in associated_personal_values:
                node_value_associations_10 = vectorise(
                    current_node["personal_values_10"]
                )
                node_value_associations_10 = np.where(
                    node_value_associations_10 < 0,
                    0 * node_value_associations_10,
                    node_value_associations_10,
                )
                dot_product = calculate_dot_product(
                    transformed_aligned_scores, node_value_associations_10
                )
                aligned_effects[get_node_id(current_node)] = dot_product

    aligned_effects = dict(
        sorted(aligned_effects.items(), key=lambda x: x[1], reverse=True)
    )

    return aligned_effects
