from collections import Counter, OrderedDict
import pickle
import random
import sys

from flask import current_app
import networkx as nx
import numpy as np

from ..scoring.build_localised_acyclic_graph import build_localised_acyclic_graph


class GetFeed:

    """
    After users have completed their survey, they want to receive personalized suggestions
    for issues that affect them and actions they can take that will directly impact those
    issues.

    This class handles the feed functions. Currently the feed works by associating
    a user's values with relevant issues (nodes).
    """

    def __init__(self, user_scores):
        self.G = current_app.config["T"].copy()  # Using test ontology
        self.user_scores = user_scores
        self.climate_effects = None

    def get_scores_vector(self):
        """
        Extracts scores from a dictionary and returns the scores as a vector (alphabetical order).
        Used in simple_scoring to compute a dot product.
        """
        return [
            self.user_scores["achievement"],
            self.user_scores["benevolence"],
            self.user_scores["conformity"],
            self.user_scores["hedonism"],
            self.user_scores["power"],
            self.user_scores["security"],
            self.user_scores["self_direction"],
            self.user_scores["stimulation"],
            self.user_scores["tradition"],
            self.user_scores["universalism"],
        ]

    def score_nodes(self, session_uuid, nx_utils, myth_processor, solution_processor):
        """
        Each climate effects node will have personal values associated with it. These
        values are stored as a vector within the node. This vector is run through the
        dot product with the users scores to determine the overall relevance of the node
        to a user's values.

        :param session_uuid: uuid4 as str
        :param nx_utils: Class to extract data from nodes
        :param myth_processor: Class to extract data from myths
        :param solution_processor: Class to extract data from solutions
        """
        climate_effects = []
        user_scores_vector = np.array(self.get_scores_vector())

        alpha = 2  # transforms user questionnaire scores to exponential distribution
        modified_user_scores_vector = np.power(user_scores_vector, alpha)
        localised_acyclic_graph = build_localised_acyclic_graph(
            self.G, session_uuid
        )  # TODO: Fix

        for node in self.G.nodes:
            current_node = self.G.nodes[node]
            if "personal_values_10" in current_node and any(
                current_node["personal_values_10"]
            ):
                node_values_associations_10 = current_node["personal_values_10"]

                myth_processor.set_current_node(current_node)
                nx_utils.set_current_node(current_node)
                d = {
                    "effectId": nx_utils.get_node_id(),
                    "effectTitle": current_node["label"],
                    "effectDescription": nx_utils.get_description(),
                    "effectShortDescription": nx_utils.get_short_description(),
                    "imageUrl": nx_utils.get_image_url(),
                    "effectSources": nx_utils.get_causal_sources(),
                    "isPossiblyLocal": nx_utils.get_is_possibly_local(
                        localised_acyclic_graph.nodes[node]
                    ),
                    "effectSpecificMythIRIs": myth_processor.get_effect_specific_myths(),
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
                    d["effectSolutions"] = solution_processor.get_user_actions(
                        current_node["label"]
                    )

                d["effectScore"] = score
                climate_effects.append(d)

        self.climate_effects = climate_effects

    def get_best_nodes(self, num_feed_cards=21):
        """
        Sorts nodes by their relevance to a user.
        Nodes with no score are assigned -inf as it could be risky to show
        a user an unreviewed climate effect (may have a backfire effect).

        :returns best_nodes: top nodes for a user
        """
        best_nodes = sorted(
            self.climate_effects,
            key=lambda k: k["effectScore"] or float("-inf"),
            reverse=True,
        )[:num_feed_cards]

        return best_nodes
