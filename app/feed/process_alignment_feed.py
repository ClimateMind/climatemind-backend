from app import db
from app.errors.errors import DatabaseError
from app.models import AlignmentFeed, Scores, Users, Conversations
from app.alignment.utils import *
from app.scoring.build_localised_acyclic_graph import get_node_id
from app.scoring.process_alignment_scores import *
from flask import current_app
from random import sample, shuffle
from app.network_x_tools.network_x_utils import network_x_utils

CONVERSATION_SOLUTION_NAME = "effective communication framing"
POPULAR_SOLUTION_NAMES = {
    "enact carbon tax policy (revenue neutral)",
    "reducing food waste",
    "composting",
    "eating lower down the food-chain (plant-rich diets)",
    "producing electricity via onshore wind turbines",
    "using high-efficiency heat pumps",
    "using improved clean cookstoves",
    "producing electricity via distributed solar photovoltaics",
    "making aviation more efficient",
}
POPULAR_SOLUTION_COUNT = 4
UNPOPULAR_SOLUTION_COUNT = 2


def create_alignment_feed(
    conversation_uuid, quiz_uuid, alignment_feed_uuid, alignment_scores_uuid
):
    """
    Calculate aligned feed based on user a and b quiz results and add to the alignment feed table.

    Parameters
    ==============
    conversation_uuid (UUID)
    quiz_uuid (UUID) - user b quiz uuid to compare scores with user a scores
    alignment_feed_uuid (UUID) - uuid created when post alignment endpoint is used
    """
    

    #TO DO make a contant variable so 3 isn't hard coded as the number of effects to show to user B.
    aligned_effects_sorted_by_shared_values = get_aligned_effects(alignment_scores_uuid, 3)

    sorted_aligned_effects = sort_aligned_effects_by_user_b_values(aligned_effects_sorted_by_shared_values, quiz_uuid)

    try:
        alignment_feed = AlignmentFeed()
        alignment_feed.alignment_feed_uuid = alignment_feed_uuid
        alignment_feed.aligned_effect_1_iri = sorted_aligned_effects[0]
        alignment_feed.aligned_effect_2_iri = sorted_aligned_effects[1]
        alignment_feed.aligned_effect_3_iri = sorted_aligned_effects[2]
        assign_alignment_iris(
            alignment_feed,
            "solution",
            find_alignment_solution_iris(
                CONVERSATION_SOLUTION_NAME,
                POPULAR_SOLUTION_NAMES,
                POPULAR_SOLUTION_COUNT,
                UNPOPULAR_SOLUTION_COUNT,
            ),
        )
        db.session.add(alignment_feed)
        db.session.commit
    except:
        raise DatabaseError(
            message="An error occurred while adding the alignment feed to the database."
        )


def get_aligned_effects(alignment_scores_uuid, n_nodes):
    """
    Create a sorted dictionary of IRIs and dot products for impacts/effects from the ontology that are positively associated with the top aligned personal
    value for users A and B (calculated based on comparison of their quiz results).

    Parameters
    ==========
    alignment_scores_uuid (UUID) - the uuid for the aligned scores for users a and b
    n_nodes (int) - the number of effect nodes to output that score the highest. Default is 3 impacts.

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
    aligned_scores_array = np.array(get_aligned_scores(aligned_scores))
    transformed_aligned_scores = transform_aligned_scores(aligned_scores_array)

    for node in G.nodes:
        current_node = G.nodes[node]

        if (
            "risk" in current_node["all classes"]
            and "test ontology" in current_node["all classes"]
            and not all([value == None for value in current_node["personal_values_10"]])
        ):
            associated_personal_values = map_associated_personal_values(
                current_node["personal_values_10"]
            )

            if top_aligned_value in associated_personal_values:
                node_value_associations_10 = np.array(
                    current_node["personal_values_10"]
                )
                adjusted_node_value_associations_10 = np.where(
                    node_value_associations_10 < 0,
                    0 * node_value_associations_10,
                    node_value_associations_10,
                )
                dot_product = np.dot(
                    transformed_aligned_scores, adjusted_node_value_associations_10
                )
                aligned_effects[get_node_id(current_node)] = dot_product

    aligned_effects = dict(
        sorted(aligned_effects.items(), key=lambda x: x[1], reverse=True)
    )

    aligned_effects_keys = list(aligned_effects.keys())
    
    aligned_effects_top_keys = []
    if len(aligned_effects_keys) > n_nodes:
        aligned_effects_top_keys = aligned_effects_keys[0:n_nodes]
    else:
        aligned_effects_top_keys = aligned_effects_keys

    # TODO: delete this check after expansion of the ontology. This repeats the topics until the list is n long as needed.
    aligned_effects_key_extra = list(aligned_effects.keys())[1]
    while len(aligned_effects_keys) < n_nodes:
        aligned_effects_top_keys.append(aligned_effects_key_extra)

    return aligned_effects_top_keys


def assign_alignment_iris(alignment_feed, field_type, iris):
    """Set the solution iri fields in the alignment feed."""
    for (index, iri) in enumerate(iris, start=1):
        setattr(alignment_feed, "aligned_{}_{}_iri".format(field_type, index), iri)


def find_alignment_solution_iris(
    conversation_name, popular_names, popular_count, unpopular_count
):
    """Choose and order solutions for the alignment.

    Using the (mitigation) solutions from the ontology, put the conversation solution first,
    followed by a random ordering of popular and unpopular solutions. This function takes no
    user-specific arguments, since solutions are (currently) independent of users' personal values
    etc.

    Parameters
    ==============
    conversation_name (str) - label of the conversation solution
    popular_names (set of str) - labels of the popular solutions
    popular_count (int) - the number of popular solutions to include
    unpopular_count (int) - the number of unpopular solutions to include

    Returns
    ==========
    List of strings: an ordered list of solution iris for an alignment feed

    """
    solution_map = {"conversation": None, "popular": set(), "unpopular": set()}
    solution_nodes = get_solution_nodes()
    nx = network_x_utils()
    for node in solution_nodes:
        name = node["label"]
        nx.set_current_node(node)
        iri = nx.get_node_id()
        if name == conversation_name:
            solution_map["conversation"] = iri
        elif name in popular_names:
            solution_map["popular"].add(iri)
        else:
            solution_map["unpopular"].add(iri)
    sample_solutions = sample(solution_map["popular"], popular_count) + sample(
        solution_map["unpopular"], unpopular_count
    )
    shuffle(sample_solutions)
    return [solution_map["conversation"]] + sample_solutions


def get_solution_nodes():
    """Find the solution nodes in the ontology."""
    G = current_app.config["G"].copy()
    solution_names = G.nodes["increase in greenhouse effect"]["mitigation solutions"]
    return [node for node in G.nodes.values() if node["label"] in solution_names]
