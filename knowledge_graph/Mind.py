import sys

from owlready2 import get_ontology
from typing import List

from knowledge_graph import make_network


Results = List[str]


class Mind:
    def __init__(self):
        self.__ontology_source = "./climate_mind_ontology"
        self.__ontology = self.__load_ontology()

    def __load_ontology(self):
        try:
            onto = get_ontology(self.__ontology_source).load()
            properties = list(onto.properties())
            [make_network.give_alias(x) for x in properties]
            return onto

        except (FileNotFoundError, IsADirectoryError, ValueError):
            raise

    def _get_ontology(self):
        try:
            if self.__ontology is None:
                raise ValueError
            return self.__ontology
        except ValueError:
            raise

    def search(self, query: str) -> Results:
        try:
            return make_network.get_edges(self._get_ontology(), query)
        except (ValueError, AttributeError):
            raise ValueError

    def multiParameterSearch(self) -> Results:
        try:
            return make_network.get_edges(self._get_ontology(), None)
        except (ValueError, AttributeError):
            raise ValueError
