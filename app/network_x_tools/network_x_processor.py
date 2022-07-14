import networkx as nx


class network_x_processor:
    def __init__(self, graph_file_name):
        self.graph_file = graph_file_name
        self.G = self.load_graph()

    def load_graph(self):
        """Loads the NetworkX representation of the Ontology from the Gpickle file."""
        try:
            G = nx.read_gpickle(self.graph_file)
            return G
        except (FileNotFoundError, IsADirectoryError, ValueError):
            raise

    def get_graph(self):
        return self.G
