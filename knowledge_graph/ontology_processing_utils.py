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
    
def _save_graph_helper(G, outfile_path, fname='Climate_Mind_DiGraph', ext='.gpickle'):
    writer = {'.gpickle':nx.write_gpickle,
              '.gexf':nx.write_gexf,
              '.gml':nx.write_gml,
              '.graphml':nx.write_graphml,
              '.yaml':nx.write_yaml,
              '.json':lambda g,f: f.write(json_graph.jit_data(g, indent=4))}
    mode = 'wb'
    if ext in ('.json','.yaml'):
        mode = 'w'
    file_path = os.path.join(outfile_path, fname + ext)
    with open(file_path, mode) as outfile:
        writer[ext](G, outfile)
    
def save_graph_to_pickle(G, outfile_path, fname='Climate_Mind_DiGraph'):
    _save_graph_helper(G, outfile_path, fname, ext='.gpickle')

def save_graph_to_gexf(G, outfile_path, fname='Climate_Mind_DiGraph'):
    _save_graph_helper(G, outfile_path, fname, ext='.gexf')

def save_graph_to_gml(G, outfile_path, fname='Climate_Mind_DiGraph'):
    _save_graph_helper(G, outfile_path, fname, ext='.gml')

def save_graph_to_graphml(G, outfile_path, fname='Climate_Mind_DiGraph'):
    _save_graph_helper(G, outfile_path, fname, ext='.graphml')

def save_graph_to_yaml(G, outfile_path, fname='Climate_Mind_DiGraph'):
    _save_graph_helper(G, outfile_path, fname, ext='.yaml')

def save_graph_to_json(G, outfile_path, fname='Climate_Mind_DiGraph'):
    _save_graph_helper(G, outfile_path, fname, ext='.json')

def save_test_ontology_to_json(G, outfile_path, fname='Climate_Mind_Digraph_Test_Ont'):
    save_graph_to_json(G, outfile_path, fname)