import sys

import networkx as nx

from ..scoring.scoring_utils import (
    get_test_ontology,
    get_valid_test_ont,
    get_non_test_ont,
)


class network_x_processor:
    def __init__(self):
        self.graph_file = "./output/Climate_Mind_DiGraph.gpickle"
        self.G = self.load_graph()

    def load_graph(self):
        """Loads the NetworkX representation of the Ontology from the Gpickle file."""
        try:
            G = nx.read_gpickle(self.graph_file)
            return G

        except (FileNotFoundError, IsADirectoryError, ValueError):
            raise

    def get_graph(self):
        """
        Returns the NetworkX representation of the Ontology if found.
        """
        try:
            if self.G is None:
                raise ValueError
            return self.G
        except ValueError:
            raise

    def get_test_graph(self):
        """
        Returns the test ontology for use in the user feed algorithm.
        """
        T = self.G.copy()
        valid_test_ont = get_valid_test_ont()
        not_test_ont = get_non_test_ont()
        get_test_ontology(T, valid_test_ont, not_test_ont)
        return T
