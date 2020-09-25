import pickle
import networkx as nx
import sys
from collections import Counter
from knowledge_graph.make_graph import (
    get_test_ontology,
    get_valid_test_ont,
    get_non_test_ont,
)


def simple_scoring(G, user_scores):
    """Each node contains a list of classes, which include the values associated with
    the node. For the simple scoring, only positively associated values are
    considered. All of the users value scores are > 0, meaning negative relationships
    are not considered.
    """
    nodes_with_scores = {}

    for node in G.nodes:
        node_classes = G.nodes[node]["direct classes"]
        set_of_values = {
            node_class.split()[0]
            for node_class in node_classes
            if node_class.split()[0] in user_scores.keys()
        }

        if set_of_values:
            score = 0
            for value in set_of_values:
                score += user_scores[value]
            nodes_with_scores[node] = score

    return nodes_with_scores


def get_best_nodes(nodes_with_scores, n):
    """Returns the top n Nodes for a user along with the scores for those nodes.

    Parameters
    ----------
    nodes_with_scores - Dictionary containing NetworkX nodes and Integer scores
    n - Integer to specify # of desired scores
    """
    best_nodes = sorted(nodes_with_scores, key=nodes_with_scores.get, reverse=True)[:3]
    return best_nodes


def get_pickle_file(filename):
    G = nx.read_gpickle(filename)
    return G


def get_user_nodes(user_scores):
    G = get_pickle_file("Climate_Mind_DiGraph.gpickle")

    valid_test_ont = get_valid_test_ont()
    not_test_ont = get_non_test_ont()

    get_test_ontology(G, valid_test_ont, not_test_ont)
    nodes_with_scores = simple_scoring(G, user_scores)
    best_nodes_for_user = get_best_nodes(nodes_with_scores, 3)
    return best_nodes_for_user
