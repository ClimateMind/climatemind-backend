import pickle
import numpy
import networkx as nx
import sys
from collections import Counter
from knowledge_graph.make_graph import (
    get_test_ontology,
    get_valid_test_ont,
    get_non_test_ont,
)

OFFSET = 4  # .edu <- to skip these characters and get the unique IRI

def remove_non_value_database_columns(scores):
    if "_sa_instance_state" in scores.keys():
        del scores["_sa_instance_state"]
    if "session_id" in scores.keys():
        del scores["session_id"]
    if "scores_id" in scores.keys():
        del scores["scores_id"]
    if "user_id" in scores.keys():
        del scores["user_id"]
    return scores


def get_effect_id(node):
    try:
        full_iri = node["iri"]
        pos = full_iri.find("edu") + OFFSET
        return full_iri[pos:]
    except:
        return "No IRI Found"

def get_short_description(node):
    try:
        return node["schema_shortDescription"]
    except:
        return "No short desc available at present"

def get_image_url(node):
    try:
        return node["properties"]["schema_image"][0]
    except:
        # Default image url if image is added
        return "https://yaleclimateconnections.org/wp-content/uploads/2018/04/041718_child_factories.jpg"

def simple_scoring(G, user_scores):
    """Each node contains a list of classes, which include the values associated with
    the node. For the simple scoring, only positively associated values are
    considered. All of the users value scores are > 0, meaning negative relationships
    are not considered.
    """
    climate_effects = []

    for node in G.nodes:
        if node == "decrease in GDP":
            print(G.nodes[node])
        try:
            set_of_values = G.nodes[node]["personal_values_10"]
            print(set_of_values)
        except:
            set_of_values = None

        if set_of_values:
            #print(G.nodes[node])

            score = 0
            #for value in set_of_values:
            #    score += user_scores[value]

            d = {
                "effectId": get_effect_id(G.nodes[node]),
                "effectTitle": G.nodes[node]["label"],
                "effectDescription": get_short_description(G.nodes[node]),
                "effectScore": score,
                "imageUrl": get_image_url(G.nodes[node]),
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
