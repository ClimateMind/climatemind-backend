import pickle
import networkx as nx
import sys
from collections import Counter
from knowledge_graph import app
from scoring.scoring_utils import (
    get_test_ontology,
    get_valid_test_ont,
    get_non_test_ont,
)
from network_x_tools.process_myths import process_myths
from network_x_tools.network_x_utils import network_x_utils
from network_x_tools.process_solutions import process_solutions

from knowledge_graph.build_localised_acyclic_graph import build_localised_acyclic_graph
import numpy as np
import random
from collections import OrderedDict


class score_nodes:

    """

    After users have completed their survey, they want to receive personalized suggestions
    for issues that affect them and actions they can take that will directly impact those
    issues.

    This class handles the scoring functions. Currently the scoring works by associating
    a user's values with relevant issues (nodes). In the future this will be expanded to
    include their location (zip code) and occupation.

    Any scoring related functions should be added here.

    """

    def __init__(self, user_scores, n, session_id):
        self.G = app.config["G"].copy()
        self.USER_SCORES = user_scores
        self.N = n  # Number of Nodes to return for user feed
        self.SESSION_ID = session_id
        self.NX_UTILS = network_x_utils()
        self.MYTH_PROCESSOR = None
        self.SOL_PROCESSOR = None
        self.ALPHA = 2  # variable for transforming user questionnaire scores to exponential distribution
        self.MAX_N_SOLUTIONS = 4
        self.RATIO = 0.5  # ratio of number of adaptation to mitigation solutions to aspire to show in the user's feed
        self.BEST_NODES = None
        self.CLIMATE_EFFECTS = None

    def get_scores_vector(self):
        """Extracts scores from a dictionary and returns the scores as a vector.

        Used in simple_scoring to compute a dot product.
        """
        return [
            self.USER_SCORES["achievement"],
            self.USER_SCORES["benevolence"],
            self.USER_SCORES["conformity"],
            self.USER_SCORES["hedonism"],
            self.USER_SCORES["power"],
            self.USER_SCORES["security"],
            self.USER_SCORES["self_direction"],
            self.USER_SCORES["stimulation"],
            self.USER_SCORES["tradition"],
            self.USER_SCORES["universalism"],
        ]

    def simple_scoring(self):
        """Each climate effects node will have personal values associated with it. These
        values are stored as a vector within the node. This vector is run through the
        dot product with the users scores to determine the overall relevance of the node
        to a user's values.
        """
        climate_effects = []
        user_scores_vector = np.array(self.get_scores_vector())
        modified_user_scores_vector = np.power(user_scores_vector, self.ALPHA)
        localised_acyclic_graph = build_localised_acyclic_graph(self.G, self.SESSION_ID)

        for node in self.G.nodes:
            current_node = self.G.nodes[node]
            if "personal_values_10" in current_node and any(
                current_node["personal_values_10"]
            ):
                node_values_associations_10 = current_node["personal_values_10"]

                self.MYTH_PROCESSOR.set_current_node(current_node)
                self.NX_UTILS.set_current_node(current_node)
                d = {
                    "effectId": self.NX_UTILS.get_node_id(),
                    "effectTitle": current_node["label"],
                    "effectDescription": self.NX_UTILS.get_description(),
                    "effectShortDescription": self.NX_UTILS.get_short_description(),
                    "imageUrl": self.NX_UTILS.get_image_url(),
                    "effectSources": self.NX_UTILS.get_causal_sources(),
                    "isPossiblyLocal": self.NX_UTILS.get_is_possibly_local(
                        localised_acyclic_graph.nodes[node]
                    ),
                    "effectSpecificMythIRIs": self.MYTH_PROCESSOR.get_effect_specific_myths(),
                }

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
                        modified_user_scores_vector,
                        modified_node_values_associations_10,
                    )
                    d["effectSolutions"] = self.SOL_PROCESSOR.get_user_actions(
                        current_node["label"]
                    )

                d["effectScore"] = score
                climate_effects.append(d)

        self.CLIMATE_EFFECTS = climate_effects

    def get_best_nodes(self):
        """Returns the top n Nodes for a user along with the scores for those nodes.
        If a node has no score, it will be assigned -inf as it could be risky to show
        a user an unreviewed climate effect. (may have a backfire effect).
        """
        best_nodes = sorted(
            self.CLIMATE_EFFECTS,
            key=lambda k: k["effectScore"] or float("-inf"),
            reverse=True,
        )[: self.N]

        self.BEST_NODES = best_nodes

    def get_user_nodes(self):
        """Returns the top n Nodes for a user feed."""

        valid_test_ont = get_valid_test_ont()
        not_test_ont = get_non_test_ont()

        get_test_ontology(self.G, valid_test_ont, not_test_ont)
        self.MYTH_PROCESSOR = process_myths()
        self.SOL_PROCESSOR = process_solutions()
        self.simple_scoring()
        self.get_best_nodes()
        return self.BEST_NODES
