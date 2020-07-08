import unittest
from .mind import Mind


class TestLoadingOntology(unittest.TestCase):
    def test_invalid_ontology_source(self):
        onto = Mind("bad")

        self.assertIsNone(onto.get_ontology())

    def test_valid_ontology_source(self):
        onto = Mind("./climate_mind_ontology")
        self.assertIsNotNone(onto.get_ontology())