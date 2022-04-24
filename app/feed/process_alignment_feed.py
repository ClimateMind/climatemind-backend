from app import db
from app.errors.errors import DatabaseError
from app.models import AlignmentFeed
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


def create_alignment_feed(conversation_uuid, quiz_uuid, alignment_feed_uuid):
    """
    Calculate aligned feed based on user a and b quiz results and add to the alignment feed table.

    The effects are not yet assigned appropriately.

    Parameters
    ==============
    conversation_uuid (UUID)
    quiz_uuid (UUID) - user b quiz uuid to compare scores with user a scores
    alignment_feed_uuid (UUID) - uuid created when post alignment endpoint is used
    """

    try:
        alignment_feed = AlignmentFeed()
        alignment_feed.alignment_feed_uuid = alignment_feed_uuid
        assign_alignment_iris(alignment_feed, "effect", find_alignment_effect_iris())
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


def assign_alignment_iris(alignment_feed, field_type, iris):
    """Set the solution iri fields in the alignment feed."""
    for (index, iri) in enumerate(iris, start=1):
        setattr(alignment_feed, "aligned_{}_{}_iri".format(field_type, index), iri)


def find_alignment_effect_iris():
    # TODO: Add logic. Currently working with hard-coded dummy values.
    return [
        "R9JAWzfiZ9haeNhHiCpTWkr",
        "R8JoXNnKTYqERwU7fblKTWB",
        "RB7k7p2iQQgKdQrkRP2MZWM",
    ]


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
