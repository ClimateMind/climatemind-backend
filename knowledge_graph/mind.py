from owlready2 import get_ontology


# class for storing ontology, load ontology method, queries
from src.knowledge_graph import make_network


class Mind:
    def __init__(self, mind_source: str):
        self.__ontology_source = mind_source
        self.__ontology = self.__load_ontology()

    def __load_ontology(self):
        try:
            onto = get_ontology(self.__ontology_source).load()
            properties = list(onto.properties())
            [make_network.giveAlias(x) for x in properties]
            return onto

        except FileNotFoundError:
            return None

        except IsADirectoryError:
            return None
    
    def get_ontology(self):
        try:
            if self.__ontology is None:
                raise ValueError
            return self.__ontology
        except ValueError:
            return None
