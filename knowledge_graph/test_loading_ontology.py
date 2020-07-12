import unittest
from .mind import Mind


class TestLoadingOntology(unittest.TestCase):
    def test_valid_ontology_source(self):
        onto = Mind()
        self.assertIsNotNone(onto.get_ontology())