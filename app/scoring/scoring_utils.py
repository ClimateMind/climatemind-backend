import networkx as nx
from networkx.readwrite import json_graph
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


def remove_non_test_nodes(T, node, valid_test_ont, not_test_ont):
    if node in T.nodes:
        is_test_ont = False
        for c in T.nodes[node]["direct classes"]:
            if c in valid_test_ont:
                is_test_ont = True
            if c in not_test_ont:
                is_test_ont = False
                break
        if not is_test_ont:
            T.remove_node(node)
        else:
            is_test_ont = False


def get_test_ontology(T, valid_test_ont, not_test_ont):
    for edge in list(T.edges):
        node_a = edge[0]
        node_b = edge[1]
        remove_non_test_nodes(T, node_a, valid_test_ont, not_test_ont)
        remove_non_test_nodes(T, node_b, valid_test_ont, not_test_ont)
