from app.models import Sessions
from app import db
from sqlalchemy import create_engine
import networkx as nx
import os
import urllib


def get_iri(full_iri):
    """Node IDs are the unique identifier in the IRI. This is provided to the
    front-end as a reference for the feed, but is never shown to the user.

    Example http://webprotege.stanford.edu/R8znJBKduM7l8XDXMalSWSl

    Parameters
    ----------
    node - A networkX node
    """
    offset = 4  # .edu <- to skip these characters and get the unique IRI
    pos = full_iri.find("edu") + offset
    return full_iri[pos:]


def get_node_id(node):
    """Node IDs are the unique identifier in the IRI. This is provided to the
    front-end as a reference for the feed, but is never shown to the user.

    Example http://webprotege.stanford.edu/R8znJBKduM7l8XDXMalSWSl

    Parameters
    ----------
    node - A networkX node
    """
    offset = 4  # .edu <- to skip these characters and get the unique IRI
    full_iri = node["iri"]
    pos = full_iri.find("edu") + offset
    return full_iri[pos:]


def check_if_valid_postal_code(session_id):

    try:
        # Find the user's postal code and cast to an integer for lookup in the lrf_data table.
        # This will need to change if postal codes with letters are added later and the data type in the lrf_data table changes.

        session_id = Sessions.query.filter_by(session_id=session_id).first()
        if not session_id.postal_code:
            return None
        else:
            postal_code = int(session_id.postal_code)

            if postal_code:

                DB_CREDENTIALS = os.environ.get("DATABASE_PARAMS")
                SQLALCHEMY_DATABASE_URI = (
                    "mssql+pyodbc:///?odbc_connect=%s"
                    % urllib.parse.quote_plus(DB_CREDENTIALS)
                )

                engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

                with engine.connect() as con:
                    # Check if postal code is in lrf_data table and create a list of values
                    result = con.execute(
                        "SELECT * FROM lrf_data WHERE lrf_data.postal_code=?",
                        (postal_code,),
                    )
                    exists_in_lrf_table = list(result.fetchone())
                    # Get the column names fromt the lrf_data table and create a list of names
                    columns = con.execute(
                        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='lrf_data'"
                    )
                    column_names = columns.fetchall()
                    column_names_list = []

                    for name in column_names:
                        column_names_list.append(name[0])

                if exists_in_lrf_table:
                    # Create a dictionary of lrf data for the specific postal code where the lrf_data table column names
                    # (the postal code and the IRIs) are the keys matched to the lrf_data table values for that postal code.
                    short_IRIs = [
                        get_iri(long_iri) for long_iri in column_names_list[1:]
                    ]

                    lrf_single_postcode_dict = dict(
                        zip(short_IRIs, exists_in_lrf_table[1:])
                    )
                    return lrf_single_postcode_dict

                else:
                    return None

    except Exception as e:
        print(e)


def get_starting_nodes(acyclic_graph):
    """
    Given a graph, find the terminal nodes (nodes that have no children with "causes_or_promotes" relationship) that are in the Test Ontology,
    and also are not in the class 'risk solution' (whether directly or indirectly) [doesn't include solution nodes].

    Parameters
    graph - an acyclic networkx graph of the climate mind ontology
    """
    starting_nodes = []
    for node in acyclic_graph.nodes:
        if not list(acyclic_graph.neighbors(node)):
            if (
                "test ontology" in acyclic_graph.nodes[node]
                and acyclic_graph.nodes[node]["test ontology"][0] == "test ontology"
            ):
                if "risk solution" in acyclic_graph.nodes[node]:
                    if (
                        "risk solution"
                        not in acyclic_graph.nodes[node]["risk solution"]
                    ):
                        starting_nodes.append(node)
                else:
                    starting_nodes.append(node)
        else:
            neighbor_nodes = acyclic_graph.neighbors(node)
            has_no_child = True
            for neighbor in neighbor_nodes:
                if acyclic_graph[node][neighbor]["type"] == "causes_or_promotes":
                    has_no_child = False
            if has_no_child:
                if (
                    "test ontology" in acyclic_graph.nodes[node]
                    and acyclic_graph.nodes[node]["test ontology"][0] == "test ontology"
                ):
                    if "risk solution" in acyclic_graph.nodes[node]:
                        if (
                            "risk solution"
                            not in acyclic_graph.nodes[node]["risk solution"]
                        ):
                            starting_nodes.append(node)
                    else:
                        starting_nodes.append(node)
    return starting_nodes


def build_localised_acyclic_graph(G, session_id):
    """
    Builds acyclic graph with all the nodes in it above the terminal nodes to have isPossiblyLocal field populated with 0 or 1,
    (0 for certainly not local, and 1 for maybe local or certainly local).

    Parameters
    G - networkx graph of the climate mind ontology
    session_id - session id from the SQL database
    """
    localised_acyclic_graph = make_acyclic(G)
    lrf_single_postcode_dict = check_if_valid_postal_code(session_id)
    if not lrf_single_postcode_dict:
        return G
    else:
        localised_acyclic_graph = add_lrf_data_to_graph(
            localised_acyclic_graph, lrf_single_postcode_dict
        )
        starting_nodes = get_starting_nodes(localised_acyclic_graph)

        visited_dictionary = {}
        for starting_node in starting_nodes:
            local_graph(starting_node, localised_acyclic_graph, visited_dictionary)

        return localised_acyclic_graph


def add_lrf_data_to_graph(graph, dict):
    graph_attributes = nx.get_node_attributes(graph, "all classes")

    lrf_to_iri_dict = {}
    for node in graph.nodes:
        lrf_to_iri_dict[get_node_id(graph.nodes[node])] = node
    for iri in dict.keys():
        if dict[iri] == False:
            nx.set_node_attributes(graph, {lrf_to_iri_dict[iri]: 0}, "isPossiblyLocal")
        if dict[iri] == True:
            nx.set_node_attributes(graph, {lrf_to_iri_dict[iri]: 1}, "isPossiblyLocal")

    return graph


def local_graph(node, graph, visited_dictionary):
    """
    Recursive function that modifies a graph node amd all the upstream parents based on if the climate change node could possibly be a local concept for the user.
    Requires the graph to have 'isPossiblyLocal' filled in with 0 or 1 based on the results of the Location Relevance Flag values.
    Parameters:
    node - node name (string) of a node in the graph
    graph - networkx graph object (MUST BE ACYCLIC!!!)
    visited_dictionary - dictionary of which nodes have been visited by the local_graph
    returns:
    0 or 1 (the value for isPossiblyLocal for the node)
    """
    if node in visited_dictionary.keys() and "isPossiblyLocal" in graph.nodes[node]:
        return graph.nodes[node]["isPossiblyLocal"]
    else:
        visited_dictionary[node] = True

    if not causal_parents(node, graph):
        nx.set_node_attributes(
            graph,
            {node: 0},
            "isPossiblyLocal",
        )
        return graph.nodes[node]["isPossiblyLocal"]
    else:
        if "isPossiblyLocal" in graph.nodes[node] and isinstance(
            graph.nodes[node]["isPossiblyLocal"], int
        ):
            [
                local_graph(parent, graph, visited_dictionary)
                for parent in causal_parents(node, graph)
            ]
            return graph.nodes[node]["isPossiblyLocal"]
        else:
            parentLabels = [
                local_graph(parent, graph, visited_dictionary)
                for parent in causal_parents(node, graph)
            ]
            nx.set_node_attributes(
                graph,
                {node: any(parentLabels)},
                "isPossiblyLocal",
            )
            return graph.nodes[node]["isPossiblyLocal"]


def make_acyclic(G):
    """
    Converts a climate mind graph into an acyclic version by removing all the feedback loop edges.
    Paramater:
    G = Networkx graph (Climate Mind graph) created from converting webprotege OWL ontology to networkx graph using functions in make_graph.py
    """
    B = G.copy()
    # identify nodes that are in the class 'feedback loop' then remove those nodes' 'caueses' edges because they start feedback loops.
    # nx.get_node_attributes(B, "direct classes")
    feedback_nodes = list()
    graph_attributes_dictionary = nx.get_node_attributes(B, "direct classes")

    for node in graph_attributes_dictionary:
        if "feedback loop" in graph_attributes_dictionary[node]:
            feedback_nodes.append(node)
    # get the 'causes' edges that lead out of the feedback_nodes
    # must only remove edges that cause increase in greenhouse gases... so only remove edges if the neighbor is of the class 'increase in atmospheric greenhouse gas'
    feedbackloop_edges = list()
    for node in feedback_nodes:
        node_neighbors = B.neighbors(node)
        for neighbor in node_neighbors:
            if (
                "increase in atmospheric greenhouse gas"
                in graph_attributes_dictionary[neighbor]
                or "root cause linked to humans"
                in graph_attributes_dictionary[neighbor]
            ):
                # should make this 'increase in atmospheric greenhouse gas' not hard coded!
                if (
                    B[node][neighbor]["type"] == "causes_or_promotes"
                ):  # should probably make this so the causes_or_promotes isn't hard coded!
                    feedbackloop_edges.append((node, neighbor))

    # remove all the feedback loop edges
    for feedbackloopEdge in feedbackloop_edges:
        nodeA = feedbackloopEdge[0]
        nodeB = feedbackloopEdge[1]
        B.remove_edge(nodeA, nodeB)

    return B
