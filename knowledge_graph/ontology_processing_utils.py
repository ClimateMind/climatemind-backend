import networkx as nx
from networkx.readwrite import json_graph
from knowledge_graph import app
import os


def get_valid_test_ont():
    return {
        "test ontology",
        "personal value",
        "achievement",
        "benevolence",
        "benevolence caring",
        "benevolence dependability",
        "conformity",
        "conformity interpersonal",
        "conformity rules",
        "face",
        "hedonism",
        "humility",
        "power",
        "power dominance",
        "power resources",
        "security",
        "security personal",
        "security societal",
        "self-direction",
        "self-direction autonomy of action",
        "self-direction autonomy of thought",
        "stimulation",
        "tradition",
        "universalism",
        "universalism concern",
        "universalism nature",
        "universalism tolerance",
    }


def get_non_test_ont():
    return {
        "value uncategorized (to do)",
        "risk solution",
        "adaptation",
        "geoengineering",
        "indirect adaptation",
        "indirect geoengineering",
        "indirect mitigration",
        "carbon pricing",
        "carbon tax",
        "emissions trading",
        "mitigation",
        "solution to indirect adaptation barrier",
        "solution to indirect mitigation barrier",
        "solution uncategorized (to do)",
    }


def remove_non_test_nodes(G, node, valid_test_ont, not_test_ont):
    if node in G.nodes:
        is_test_ont = False
        for c in G.nodes[node]["direct classes"]:
            if c in valid_test_ont:
                is_test_ont = True
            if c in not_test_ont:
                is_test_ont = False
                break
        if not is_test_ont:
            G.remove_node(node)
        else:
            is_test_ont = False


def get_test_ontology(G, valid_test_ont, not_test_ont):
    for edge in list(G.edges):
        node_a = edge[0]
        node_b = edge[1]
        remove_non_test_nodes(G, node_a, valid_test_ont, not_test_ont)
        remove_non_test_nodes(G, node_b, valid_test_ont, not_test_ont)


def give_alias(property_object):
    label_name = property_object.label[0]
    label_name = label_name.replace("/", "_or_")
    label_name = label_name.replace(" ", "_")
    label_name = label_name.replace(":", "_")
    property_object.python_name = label_name
    return label_name


def _save_graph_helper(G, outfile_path, fname="Climate_Mind_DiGraph", ext=".gpickle"):
    writer = {
        ".gpickle": nx.write_gpickle,
        ".gexf": nx.write_gexf,
        ".gml": nx.write_gml,
        ".graphml": nx.write_graphml,
        ".yaml": nx.write_yaml,
        ".json": lambda g, f: f.write(json_graph.jit_data(g, indent=4)),
    }
    mode = "wb"
    if ext in (".json", ".yaml"):
        mode = "w"
    file_path = os.path.join(outfile_path, fname + ext)
    with open(file_path, mode) as outfile:
        writer[ext](G, outfile)


def save_graph_to_pickle(G, outfile_path, fname="Climate_Mind_DiGraph"):
    _save_graph_helper(G, outfile_path, fname, ext=".gpickle")


def save_graph_to_gexf(G, outfile_path, fname="Climate_Mind_DiGraph"):
    _save_graph_helper(G, outfile_path, fname, ext=".gexf")


def save_graph_to_gml(G, outfile_path, fname="Climate_Mind_DiGraph"):
    _save_graph_helper(G, outfile_path, fname, ext=".gml")


def save_graph_to_graphml(G, outfile_path, fname="Climate_Mind_DiGraph"):
    _save_graph_helper(G, outfile_path, fname, ext=".graphml")


def save_graph_to_yaml(G, outfile_path, fname="Climate_Mind_DiGraph"):
    _save_graph_helper(G, outfile_path, fname, ext=".yaml")


def save_graph_to_json(G, outfile_path, fname="Climate_Mind_DiGraph"):
    _save_graph_helper(G, outfile_path, fname, ext=".json")


def save_test_ontology_to_json(G, outfile_path, fname="Climate_Mind_Digraph_Test_Ont"):
    save_graph_to_json(G, outfile_path, fname)
