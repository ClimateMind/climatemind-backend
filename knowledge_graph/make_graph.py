import networkx as nx
import pandas as pd
from make_network import give_alias
from owlready2 import *

# Load ontology and format into Python readable names
onto = get_ontology("../../Bx50aIKwEALYNmYl0CFzNp.owl").load()
obj_properties = list(onto.object_properties())
annot_properties = list(onto.annotation_properties())
[give_alias(x) for x in obj_properties]
[give_alias(x) for x in annot_properties]


# Read in the triples data
df = pd.read_csv('output.csv')

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




G = nx.DiGraph() #there should not be duplicate edges that go the same direction in the ontology. if so, need to throw an error.
edges = []
for rows in df.itertuples():
    my_list = [rows.subject, rows.object, rows.predicate]
    edges.append(my_list)

#add edges
for index in range(len(edges)):
    G.add_edge(edges[index][0],edges[index][1],type=edges[index][2], properties = None)

#bind each node in the Networkx DiGraph to the associated node object from the Owlready2 ontology.
#add all class from the Owlready2 ontology to each node of graph G
for node in list(G.nodes):
    ontology_node = onto.search_one(label = node)
    class_objects = onto.get_parents_of(ontology_node)
    annot_properties = [thing.label[0].replace(":","_") for thing in list(onto.annotation_properties())]
    G.add_nodes_from([node], individual = ontology_node)
    G.add_nodes_from([node], comment = ontology_node.comment)
    G.add_nodes_from([node], classes = set([parent.label[0] for parent in class_objects if parent in onto.classes()])) #the if statement is needed to avoid the Restriction objects
        #still don't know why Restriction Objects are in our ontology!
        #technically each class could have multiple labels, but this way just pulling 1st label
    annot_properties_dict={}
    for prop in annot_properties:
        annot_properties_dict[prop] = set(eval("ontology_node."+prop))
    G.add_nodes_from([node], properties = annot_properties_dict)


#add edge annotation properties that exist on both nodes of an edge. And remove it from the Networkx node property dictionary.
to_remove = {}
for edge in list(G.edges):
    node_a = edge[0]
    node_b = edge[1]
    for prop in G.nodes[node_a]["properties"].keys():
        intersection = G.nodes[node_a]["properties"][prop] & G.nodes[node_b]["properties"][prop]
        #add intersection to edge property dictionary
        if intersection:
            G.add_edge(node_a,node_b,properties={prop:intersection})
            if (node_a,prop) in to_remove.keys():
                to_remove[(node_a,prop)] = to_remove[(node_a,prop)]|intersection
            else:
                to_remove[(node_a,prop)] = intersection
            if (node_b,prop) in to_remove.keys():
                to_remove[(node_b,prop)] = to_remove[(node_b,prop)]|intersection
            else:
                to_remove[(node_b,prop)] = intersection

#remove properties form Networkx nodes that occur on both nodes of an edge (because it marks that property is only for the edge)
for item in to_remove.keys():
    node = item[0]
    prop = item[1]
    to_delete = to_remove[item]
    G.nodes[node]["properties"][prop] = set(G.nodes[node]["properties"][prop] - set(to_delete))
