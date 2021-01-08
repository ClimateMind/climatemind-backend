from knowledge_graph.models import Sessions
from knowledge_graph import db
from knowledge_graph.make_graph import make_acyclic
from sqlalchemy import create_engine
import networkx as nx
import os
import urllib


def check_if_valid_postal_code(session_id):
    try:
        # Find the user's postal code and cast to an integer for lookup in the lrf_data table.
        # This will need to change if postal codes with letters are added later and the data type in the lrf_data table changes.
        session_id = Sessions.query.filter_by(session_id=session_id).first()
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
                lrf_single_postcode_dict = dict(
                    zip(column_names_list, exists_in_lrf_table)
                )
                return lrf_single_postcode_dict

            else:
                return None

    except Exception as e:
        print(e)


def build_localised_acyclic_graph(G, session_id):
    localised_acyclic_graph = make_acyclic(G)
    lrf_single_postcode_dict = check_if_valid_postal_code(session_id)

    def recursive_populating(updated_graph):
        for node in updated_graph.nodes():
            descendant_check = nx.descendants(updated_graph, node)
            if not descendant_check:
                populate_is_possibly_local(updated_graph, node)

    if lrf_single_postcode_dict:
        updated_graph = add_lrf_data_to_graph(
            localised_acyclic_graph, lrf_single_postcode_dict
        )
        localised_acyclic_graph = recursive_populating(updated_graph)

        return localised_acyclic_graph

    else:
        return localised_acyclic_graph


node_visited_dict = dict()


def add_lrf_data_to_graph(graph, dict):
    graph_attributes = nx.get_node_attributes(graph, "all classes")

    effects = []
    for node in graph_attributes:
        if "risk" in graph_attributes[node]:
            effects.append(node)

    nodes_with_lrf_data = []

    for effect in effects:
        # Match iri format to lrf_data table format
        iri = ("http://" + graph.nodes[effect]["iri"]).replace("edu.", "edu/")
        if iri in dict:
            if dict[iri] == False:
                nx.set_node_attributes(graph, {effect: 0}, "isPossiblyLocal")
            else:
                nx.set_node_attributes(graph, {effect: 1}, "isPossiblyLocal")

            node_visited_dict[effect] = 1
        else:
            continue

    return graph


def populate_is_possibly_local(updated_graph, node):

    # If node has been visited, check next node.
    if node in node_visited_dict:
        pass
    else:
        # Check predecessors.
        predecessor_nodes = updated_graph.predecessors(node)

        # Case: node has no predecessors.
        if not predecessor_nodes:
            nx.set_node_attributes(updated_graph, {node: 1}, "isPossiblyLocal")
            node_visited_dict[node] = 1
        else:
            # Build dictionary of predecessors
            predecessor_dict = dict()
            for predecessor in predecessor_nodes:
                if updated_graph[predecessor][node]["type"] == "causes_or_promotes":
                    if "isPossiblyLocal" in updated_graph.nodes[predecessor]:
                        value = updated_graph.nodes[predecessor]["isPossiblyLocal"]
                    else:
                        value = None
                    predecessor_dict[predecessor] = value
            if (
                not "isPossiblyLocal" in updated_graph.nodes[node]
                and len(predecessor_dict) == 1
            ):
                if predecessor_dict[predecessor] == 1:
                    # Case: one predecessor with isPossiblyLocal marked as 1
                    nx.set_node_attributes(updated_graph, {node: 1}, "isPossiblyLocal")
                    node_visited_dict[node] = 1
                    populate_is_possibly_local(updated_graph, predecessor)
                elif predecessor_dict[predecessor] == 0:
                    # Case: one predecessor with isPossiblyLocal marked as 0
                    nx.set_node_attributes(updated_graph, {node: 0}, "isPossiblyLocal")
                    node_visited_dict[node] = 1
                    populate_is_possibly_local(updated_graph, predecessor)
                else:
                    # Case: one predecessor with no value for isPossiblyLocal
                    populate_is_possibly_local(updated_graph, predecessor)
            else:
                if (
                    not "isPossiblyLocal" in updated_graph[node]
                    and 1 in predecessor_dict.values()
                ):
                    # Case: more than one predecessor, at least one with isPossiblyLocal marked as 1
                    true_predecessors = []
                    for predecessor in predecessor_dict:
                        if predecessor_dict[predecessor] == 1:
                            true_predecessors.append(predecessor)

                    predecessor = true_predecessors[0]
                    nx.set_node_attributes(updated_graph, {node: 1}, "isPossiblyLocal")
                    node_visited_dict[node] = 1
                    populate_is_possibly_local(updated_graph, predecessor)

                elif (
                    not "isPossiblyLocal" in updated_graph[node]
                    and 0 in predecessor_dict.values()
                ):
                    # Case: more than one predecessor, at least one with isPossiblyLocal marked as 0, no 1s
                    false_predecessors = []
                    for predecessor in predecessor_dict:
                        if predecessor_dict[predecessor] == 0:
                            false_predecessors.append(predecessor)

                    predecessor = false_predecessors[0]
                    nx.set_node_attributes(updated_graph, {node: 1}, "isPossiblyLocal")
                    node_visited_dict[node] = 1
                    populate_is_possibly_local(updated_graph, predecessor)

                else:
                    # Case: more than one predecessor, no values
                    none_predecessors = []
                    for predecessor in predecessor_dict:
                        none_predecessors.append(predecessor)
                    breakpoint()
                    predecessor = none_predecessors[0]
                    populate_is_possibly_local(updated_graph, predecessor)


"""
has no predecessors:
    - mark the value as 1
    - mark the node as visited
    - go back to the starting node

has one predecessor with a value
    - mark the predecessor's value as the current's value
    - mark the current node as visited
    - call the function using the predecessor as the current node

has one predecessor with no value:
    - call the function using the predecessor as the current node

has more than one predecessor with no values:
    - call the function using the first predecessor as the current node

has more than one predecessor with different values, with a 1:
    - mark the current node's value as 1
    - mark the node as visited
    - call the function 

has more than one predecessor with where at least one has a 0 and there are no 1s:
    - mark the current node's value as 0
    - mark the node as visited
    - call the function using the predecessor with value 1 as the current node
"""
