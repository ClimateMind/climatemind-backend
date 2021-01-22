import sys

import networkx as nx


class network_x_processor:
    def __init__(self):
        self.graph_file = "./gpickle/Climate_Mind_DiGraph.gpickle"
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
