import networkx as nx
from networkx.readwrite import json_graph
import os


def give_alias(property_object):
    label_name = property_object.label[0]
    label_name = label_name.replace("/", "_or_")
    label_name = label_name.replace(" ", "_")
    label_name = label_name.replace(":", "_")
    property_object.python_name = label_name
    return label_name
    
def save_graph_to_pickle(G, outfile_path):
    file_path = os.path.join(outfile_path, "Climate_Mind_DiGraph.gpickle")
    with open(file_path, "wb") as outfile:
        nx.write_gpickle(G, outfile)

def save_graph_to_gexf(G, outfile_path):
    file_path = os.path.join(outfile_path, "Climate_Mind_DiGraph.gexf")
    with open(file_path, "wb") as outfile:
        nx.write_gexf(G, outfile)

def save_graph_to_gml(G, outfile_path):
    file_path = os.path.join(outfile_path, "Climate_Mind_DiGraph.gml")
    with open(file_path, "wb") as outfile:
        nx.write_gml(G, outfile)

def save_graph_to_graphml(G, outfile_path):
    file_path = os.path.join(outfile_path, "Climate_Mind_DiGraph.graphml")
    with open(file_path, "wb") as outfile:
        nx.write_graphml(G, outfile)

def save_graph_to_yaml(G, outfile_path):
    file_path = os.path.join(outfile_path, "Climate_Mind_DiGraph.yaml")
    with open(file_path, "w") as outfile:
        nx.write_yaml(G, outfile)

def save_graph_to_json(G, outfile_path):
    file_path = os.path.join(outfile_path, "Climate_Mind_DiGraph.json")
    with open(file_path, "w") as outfile:
        outfile.write(json_graph.jit_data(G, indent=4))

def save_test_ontology_to_json(G, outfile_path):
    file_path = os.path.join(outfile_path, "Climate_Mind_Digraph_Test_Ont.json")
    with open(file_path, "w") as outfile:
        outfile.write(json_graph.jit_data(G, indent=4))