import networkx as nx

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



def causal_parents(node, graph):
    """
    Returns the nodes (string names) that are causal parents of the node (have the edge type "causes_or_promotes"), else returns empty list.
    Parameters
    node - name of the node (string)
    graph - networkx graph object
    """
    node_causal_parents = []
    if list(graph.predecessors(node)):
        possibleCausalParents = graph.predecessors(node)
        for possibleCausalParent in possibleCausalParents:
            if graph[possibleCausalParent][node]["type"] == "causes_or_promotes":
                node_causal_parents.append(possibleCausalParent)
    return node_causal_parents



def local_graph(node, graph, visited_dictionary):
    """
    Recursive function that modifies a graph node and all the upstream parents based on if the climate change node could possibly be a local concept for the user.
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

