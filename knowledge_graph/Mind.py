import sys

from owlready2 import get_ontology
import networkx as nx
from typing import List

from knowledge_graph import ontology_processing_utils


Results = List[str]


class Mind:
    def __init__(self):
        self.__ontology_source = "./Climate_Mind_DiGraph.gpickle"
        self.G = self.__load_ontology()

    def __load_ontology(self):
        """Loads the NetworkX representation of the Ontology from the Gpickle file."""
        try:
            G = nx.read_gpickle(self.__ontology_source)
            return G

        except (FileNotFoundError, IsADirectoryError, ValueError):
            raise

    def _get_ontology(self):
        """
        Returns the NetworkX representation of the Ontology if found.
        """
        try:
            if self.__ontology is None:
                raise ValueError
            return self.__ontology
        except ValueError:
            raise

    def search(self, query: str) -> Results:
        """ Returns data for one node in the NetworkX Object
        
        Parameters
        ----------
        query - The name of the node (str)
        """
        try:
            for node in self.G.nodes:
                if self.G.nodes[node]["label"] == query:
                    return self.G.nodes[node]
        except (ValueError, AttributeError):
            raise ValueError
