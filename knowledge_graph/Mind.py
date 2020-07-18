from owlready2 import get_ontology
from knowledge_graph import make_network
from typing import List

Results = List[str]


class Mind:
    def __init__(self):
        self.__ontology_source = "./climate_mind_ontology"
        self.__ontology = self.__load_ontology()

    def __load_ontology(self):
        try:
            onto = get_ontology(self.__ontology_source).load()
            properties = list(onto.properties())
            [make_network.giveAlias(x) for x in properties]
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
            return make_network.searchNode(self._get_ontology(), query)
        except (ValueError, AttributeError):
            raise ValueError
