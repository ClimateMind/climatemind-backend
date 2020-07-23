import networkx as nx
import pandas as pd
from make_network import give_alias
from owlready2 import *

# Read in the triples data
df = pd.read_csv('output.csv')

# Load ontology and format into Python readable names
onto = get_ontology("../../Bx50aIKwEALYNmYl0CFzNp.owl").load()
obj_properties = list(onto.object_properties())
annot_properties = list(onto.annotation_properties())
[give_alias(x) for x in obj_properties]
[give_alias(x) for x in annot_properties]

# Create a graph with multiple directional edges.
graph = nx.MultiDiGraph()

def add_node_to_graph(node_name):
    """ Takes a node, finds the relevant node in the ontology, and
        links it to the Digraph node.
        
        Parameters
        ----------
        node_name: A string representing the node
    """
    ontology_node = onto.search_one(label=node_name)
    schema = ontology_node.schema_organizationSource
    comment = ontology_node.comment
    graph.add_node(
                node_name, 
                schema=schema, 
                comment=comment,
                reference=ontology_node
                )    

# Add all nodes and edges from the dataframe to the graph
for index, row in df.iterrows():
    subject = row['subject']
    object = row['object']
    predicate = row['predicate']
    
    if subject not in graph:
        add_node_to_graph(subject)
    
    if object not in graph:
        add_node_to_graph(object)
    
    graph.add_edge(subject, object, edge_type=predicate)

def test_check_for_node(node_name):
    if node_name in graph:
        print(graph.nodes[node_name])
    
test_check_for_node('human population growth')
    