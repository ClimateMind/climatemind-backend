import pickle
import networkx as nx
import sys
from collections import Counter
from knowledge_graph.make_graph import (
    get_test_ontology,
    get_valid_test_ont,
    get_non_test_ont,
)
import numpy as np


def get_effect_id(node):
    """Effect IDs are the unique identifier in the IRI. This is provided to the
    front-end as a reference for the feed, but is never shown to the user.

    Example http://webprotege.stanford.edu/R8znJBKduM7l8XDXMalSWSl

    Parameters
    ----------
    node - A networkX node
    """
    offset = 4  # .edu <- to skip these characters and get the unique IRI
    full_iri = node["iri"]
    pos = full_iri.find("edu") + offset
    return full_iri[pos:]


def get_description(node):
    """Long Descriptions are used by the front-end to display explanations of the
    climate effects shown in user feeds.

    Parameters
    ----------
    node - A networkX node
    """
    try:
        return node["properties"]["schema_longDescription"][0]
    except:
        return "No long desc available at present"


def get_short_description(node):
    """Short Descriptions are used by the front-end to display explanations of the
    climate effects shown in user feeds.

    Parameters
    ----------
    node - A networkX node
    """
    try:
        return node["properties"]["schema_shortDescription"][0]
    except:
        return "No short desc available at present"


def get_image_url(node):
    """Images are displayed to the user in the climate feed to accompany an explanation
    of the climate effects. The front-end is provided with the URL and then requests
    these images from our server.

    Parameters
    ----------
    node - A networkX node
    """
    try:
        return node["properties"]["schema_image"][0]
    except:
        # Default image url if image is added
        return "https://yaleclimateconnections.org/wp-content/uploads/2018/04/041718_child_factories.jpg"


def get_scores_vector(user_scores):
    """Extracts scores from a dictionary and returns the scores as a vector.

    Used in simple_scoring to compute a dot product.

    Parameters
    ----------
    user_scores - Dictionary of Scores
    """
    return [
        user_scores["achievement"],
        user_scores["benevolence"],
        user_scores["conformity"],
        user_scores["hedonism"],
        user_scores["power"],
        user_scores["security"],
        user_scores["self_direction"],
        user_scores["stimulation"],
        user_scores["tradition"],
        user_scores["universalism"],
    ]


OFFSET = 4  # .edu <- to skip these characters and get the unique IRI
ALPHA = (
    2  # variable for transforming user questionnaire scores to exponential distribution
)


def simple_scoring(G, user_scores):
    """Each climate effects node will have personal values associated with it. These
    values are stored as a vector within the node. This vector is run through the
    dot product with the users scores to determine the overall relevance of the node
    to a user's values.

    Parameters
    ----------
    G - A NetworkX Graph
    user_scores - A dictionary of personal values (keys) and scores (values)
    """
    climate_effects = []
    user_scores_vector = np.array(get_scores_vector(user_scores))
    modified_user_scores_vector = np.power(user_scores_vector, ALPHA)

    for node in G.nodes:
        if "personal_values_10" in G.nodes[node]:
            node_values_associations_10 = G.nodes[node]["personal_values_10"]

            if any(v is None for v in node_values_associations_10):
                score = None
            else:
                node_values_associations_10 = np.array(node_values_associations_10)
                # double the magnitude of the backfire-effect representation:
                modified_node_values_associations_10 = np.where(
                    node_values_associations_10 < 0,
                    2 * node_values_associations_10,
                    node_values_associations_10,
                )
                score = np.dot(
                    modified_user_scores_vector, modified_node_values_associations_10
                )
            d = {
                "effectId": get_effect_id(G.nodes[node]),
                "effectTitle": G.nodes[node]["label"],
                "effectDescription": get_description(G.nodes[node]),
                "effectShortDescription": get_short_description(G.nodes[node]),
                "effectScore": score,
                "imageUrl": get_image_url(G.nodes[node]),
                "actionHeadline": "Reducing Food Waste",  # TODO Add actual actions
            }
            climate_effects.append(d)

    return climate_effects


def get_best_nodes(climate_effects, n):
    """Returns the top n Nodes for a user along with the scores for those nodes.
    If a node has no score, it will be assigned -inf as it could be risky to show
    a user an unreviewed climate effect. (may have a backfire effect).

    Parameters
    ----------
    nodes_with_scores - Dictionary containing NetworkX nodes and Integer scores
    n - Integer to specify # of desired scores
    """
    best_nodes = sorted(
        climate_effects, key=lambda k: k["effectScore"] or float("-inf"), reverse=True
    )[:5]
    return best_nodes


def get_pickle_file(filename):
    G = nx.read_gpickle(filename)
    return G


def get_user_nodes(user_scores):
    G = get_pickle_file("Climate_Mind_DiGraph.gpickle")

    valid_test_ont = get_valid_test_ont()
    not_test_ont = get_non_test_ont()

    get_test_ontology(G, valid_test_ont, not_test_ont)
    climate_effects = simple_scoring(G, user_scores)
    best_nodes_for_user = get_best_nodes(climate_effects, 3)
    return best_nodes_for_user
