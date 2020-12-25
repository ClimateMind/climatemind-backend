"""
The purpose of this script is to regression test refactoring of the owl->nx 
processing pipeline. Concretely, this checks that the output gpickle files
represent equivalent graphs, ignoring node or edge attributes that are lists
that differ only in the order of their contents.

To use this script:
    1. Execute `python process_new_ontology_file.py` using the un-refactored code (i.e. master branch) 
    2. Append '.bck.' to the filename of the output gpickle file.
    3. Checkout to the refactored branch.
    4. Execute `python process_new_ontology_file.py`
    5. Execute this script to compare the contents of the two graphs. 
    
If the graphs don't satisfy the equality conditions described above, an assertion error will be thrown. 
If the script executes successfully with no return value or exceptions, all tests were successful.
"""

import networkx as nx
from networkx.readwrite.gpickle import read_gpickle


def test_node_attributes(collection1, collection2):
    for item1_id, item1_data in collection1:
        item2_data = collection2[item1_id]
        assert item1_data.keys() == item2_data.keys()
        for k, v1 in item1_data.items():
            v2 = item2_data[k]
            assert set(v1) == set(v2)


def test_edge_attributes(g_old, g_new):
    for src_old, tgt_old, data_old in g_old.edges(data=True):
        data_new = g_new.edges()[src_old, tgt_old]
        assert data_old.keys() == data_new.keys()
        for k, v1 in data_old.items():
            v2 = data_new[k]
            try:
                assert set(v1) == set(v2)
            except TypeError:
                assert v1 is None
                assert v2 is None


fname = "Climate_Mind_DiGraph.gpickle"
g_old = read_gpickle(fname + ".bck")
g_new = read_gpickle(fname)

assert len(g_old) == len(g_new)
assert len(g_old.edges()) == len(g_new.edges())

test_node_attributes(g_old.nodes(data=True), g_new.nodes(data=True))
test_node_attributes(g_new.nodes(data=True), g_old.nodes(data=True))
test_edge_attributes(g_old, g_new)
test_edge_attributes(g_new, g_old)
