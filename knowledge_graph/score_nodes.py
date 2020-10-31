import pickle
import networkx as nx
import sys
from collections import Counter
from knowledge_graph.make_graph import (
    get_test_ontology,
    get_valid_test_ont,
    get_non_test_ont,
)

OFFSET = 4  # .edu <- to skip these characters and get the unique IRI


def simple_scoring(G, user_scores):
    """Each node contains a list of classes, which include the values associated with
    the node. For the simple scoring, only positively associated values are
    considered. All of the users value scores are > 0, meaning negative relationships
    are not considered.
    """
    climate_effects = []

    for node in G.nodes:
        node_classes = G.nodes[node]["direct classes"]
        set_of_values = {
            node_class.split()[0]
            for node_class in node_classes
            if node_class.split()[0] in user_scores.keys()
        }

        if set_of_values:
            print(G.nodes[node])
            full_iri = G.nodes[node]["iri"]
            pos = full_iri.find("edu") + OFFSET
            effect_id = full_iri[pos:]

            score = 0
            for value in set_of_values:
                score += user_scores[value]

            try:
                desc = G.nodes[node]["schema_shortDescription"]
            except:
                desc = "No short desc available at present"

            try:
                imageUrl = G.nodes[node]["properties"]["schema_image"][0]
            except:
                # Default image url if image is added
                imageUrl = "https://yaleclimateconnections.org/wp-content/uploads/2018/04/041718_child_factories.jpg"

            d = {
                "effectId": effect_id,
                "effectTitle": G.nodes[node]["label"],
                "effectDescription": desc,
                "effectScore": score,
                "imageUrl": imageUrl,
            }
            climate_effects.append(d)

    return climate_effects


def get_best_nodes(climate_effects, n):
    """Returns the top n Nodes for a user along with the scores for those nodes.

    Parameters
    ----------
    nodes_with_scores - Dictionary containing NetworkX nodes and Integer scores
    n - Integer to specify # of desired scores
    """
    best_nodes = sorted(climate_effects, key=lambda k: k["effectScore"], reverse=True)[
        :3
    ]
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
