import json
import pickle
import argparse
import networkx as nx
import pandas as pd

from owlready2 import *
from networkx.readwrite import json_graph

from make_network import give_alias


# Set a lower JVM memory limit
owlready2.reasoning.JAVA_MEMORY = 500

def convert_dataframe_to_edges(df):
    """ 
        Convert dataframe to edges
        
        Parameters
        ----------
        df: A dataframe of object, subject, predicate triples
    """
    edges = []
    for rows in df.itertuples():
        edge_list = [rows.subject, rows.object, rows.predicate]
        edges.append(edge_list)
    return edges



def add_edges_to_graph(edges, G):
    """ 
        Adds edges to networkx object
        
        Parameters
        ----------
        edges: List of graph edges (object, subject, predicate triples)
        G: A networkx Graph
    """
    for index in range(len(edges)):
        G.add_edge(
                   edges[index][0],
                   edges[index][1],
                   type=edges[index][2],
                   properties=None
                   )


def add_ontology_data_to_graph_nodes(G, onto):
    """ Find the equivalent nodes in the ontology and load in relevant data
        including the classes they belong to.
        
        Parameters
        ----------
        G: A networkx Graph
        onto: owlready2 ontology object
        """
    for node in list(G.nodes):
        ontology_node = onto.search_one(label = node)
        class_objects = onto.get_parents_of(ontology_node)
        annot_properties = [thing.label[0].replace(":","_") for thing in list(onto.annotation_properties())]
        
        #need to add here and replace the hard coding of 'classes' with each of the child classes of the class "Climate Mind". See http://owlready.8326.n8.nabble.com/Ontology-tree-td1178.html
        #also need to add in automated reasoning so that the classes aren't nested.
        
        #superclasses = list(Thing.subclasses())
        #['status - source etc']
        #['status - value']
        #['climate mind']
        #['misleading information']
        
        #CM_class = superclasses[2] #this is hard coded. would break if top structure of ontology changes... should probably just search for the class 'climate mind'.
        cm_class = onto.search_one(label = 'climate mind')
        superclasses = list(cm_class.subclasses())
        superclass_labels = [superclass_object.label for superclass_object in superclasses]
        #cm_class.ancestors()
        #cm_class.descendants()
        #cm_class.get_parents_of()
        
        
        #make dictionary to add proper attributes to the node
        
        attributes_dict = {}
        attributes_dict['label'] = str(ontology_node.label[0])
        attributes_dict['iri'] = str(ontology_node)
        attributes_dict['comment'] = str(ontology_node.comment)
        attributes_dict['direct classes'] = [str(parent.label[0]) for parent in class_objects if parent in onto.classes()]
        
        all_classes = []
        for parent in class_objects:
            if parent in onto.classes():
                all_classes.extend(parent.ancestors())

        list_classes = [str(node_object.label[0]) for node_object in all_classes if node_object in onto.classes()]
        list_classes = list(set(list_classes))
        if 'climate mind' in list_classes:
            list_classes.remove('climate mind')
        attributes_dict['all classes'] = list_classes

        #for each class in the classes associated with the node, list that class in the appropriate super_class in the attributes_dict and all of the ancestor classes of that class
        for node_class in class_objects:
            for super_class in superclasses:
                if node_class in super_class.descendants():
                    #descendants() includes self class, but excludes non-entity classes such as restrictions
                    to_add = [str(thing.label[0]) for thing in node_class.ancestors() if thing in onto.classes()]
                    if 'climate mind' in to_add:
                        to_add.remove('climate mind')
                    if super_class in attributes_dict.keys():
                        attributes_dict[str(super_class.label[0])] = list(set(attributes_dict[super_class]) | set( to_add ))
                    else:
                        attributes_dict[str(super_class.label[0])] = to_add
        #if there are multiple of the nested classes associated with the node in the ontology, code ensures it doesn't overwrite the other class.

        G.add_nodes_from([(node, attributes_dict)])

        #the if statement is needed to avoid the Restriction objects
        #still don't know why Restriction Objects are in our ontology!
        #technically each class could have multiple labels, but this way just pulling 1st label

        annot_properties_dict={}
        for prop in annot_properties:
            annot_properties_dict[prop] = list(eval("ontology_node."+prop))
        G.add_nodes_from([node], properties = annot_properties_dict)


def set_edge_properties(G):
    """ Add edge annotation properties that exist on both nodes of an edge
        and create a list of properties to remove from the nodes.
        (Properties that exist on both nodes of an edge are only for the edge)
        
        Parameters
        ----------
        G: A networkx Graph
        """
    to_remove = {}
    for edge in list(G.edges):
        node_a = edge[0]
        node_b = edge[1]
        for prop in G.nodes[node_a]["properties"].keys():
            intersection = set(G.nodes[node_a]["properties"][prop]) & set(G.nodes[node_b]["properties"][prop])
            #add intersection to edge property dictionary
            if intersection:
                G.add_edge(node_a,node_b,properties={prop:list(intersection)})
                if (node_a,prop) in to_remove.keys():
                    to_remove[(node_a,prop)] = to_remove[(node_a,prop)]|intersection
                else:
                    to_remove[(node_a,prop)] = intersection
                if (node_b,prop) in to_remove.keys():
                    to_remove[(node_b,prop)] = to_remove[(node_b,prop)]|intersection
                else:
                    to_remove[(node_b,prop)] = intersection
    return list(to_remove)


def remove_edge_properties_from_nodes(G, to_remove):
    """ Remove properties from Networkx nodes that occur on both nodes of an edge
        (because it marks that property is only for the edge).
        
        Parameters
        ----------
        G: A networkx graph
        to_remove: A dictionary of nodes and properties
        """
    for item in to_remove:
        node = item[0]
        prop = item[1]
        to_delete = item
        G.nodes[node]["properties"][prop] = [node for node in list(G.nodes[node]["properties"][prop])
                                                if node not in list(to_delete)]

def save_graph_to_pickle(G):
    with open('Climate_Mind_DiGraph.gpickle', 'wb') as outfile:
        nx.write_gpickle(G, outfile)

def save_graph_to_gexf(G):
    with open('Climate_Mind_DiGraph.gexf', 'wb') as outfile:
        nx.write_gexf(G, outfile)

def save_graph_to_gml(G):
    with open('Climate_Mind_DiGraph.gml', 'wb') as outfile:
        nx.write_gml(G, outfile)

def save_graph_to_graphml(G):
    with open('Climate_Mind_DiGraph.graphml', 'wb') as outfile:
        nx.write_graphml(G, outfile)

def save_graph_to_yaml(G):
    with open('Climate_Mind_DiGraph.yaml', 'w') as outfile:
        nx.write_yaml(G, outfile)

def save_graph_to_json(G):
    with open('Climate_Mind_DiGraph.json', 'w') as outfile:
        outfile.write(json_graph.jit_data(G, indent=4))
        
def save_test_ontology_to_json(G):
    with open('Climate_Mind_Digraph_Test_Ont.json', 'w') as outfile:
        outfile.write(json_graph.jit_data(G, indent=4))


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



# Read the JSON file back
def read_json_file(filename):
    with open(filename) as f:
        js_graph = json.load(f)
    return js_graph

# Test reading JSON file & print the nodes
#G2 = read_json_file("Climate_Mind_DiGraph.json")
#print(json.dumps(G2, indent=4, sort_keys=True))

# Test reading JSON file & print the nodes for Test Ontology Only
# G2 = read_json_file("../Climate_Mind_DiGraph_Test_Ont.json")
# print(json.dumps(G2, indent=4, sort_keys=True))

def main(args):
    """
    Main function to make networkx graph object from reference ontology and edge list.
    
    input: args = args from the argument parser for the function
                    (refOntologyPath, refEdgeListPath)
    output: saves a python pickle file of the networkx object, and yaml and json of the networkx object
    
    example: python3 make_graph.py "./climate_mind_ontology20200721.owl" "output.csv"
    """
    
    #set arguments
    onto_path = args.refOntologyPath
    edge_path = args.refEdgeListPath
    
    # Load ontology and format object properties and annotation properties into Python readable names
    onto = get_ontology(onto_path).load()
    obj_properties = list(onto.object_properties())
    annot_properties = list(onto.annotation_properties())
    [give_alias(x) for x in obj_properties]
    [give_alias(x) for x in annot_properties]

    #run automated reasoning
    with onto:
        sync_reasoner()
    #print(list(default_world.inconsistent_classes()))
    
    # Read in the triples data
    df = pd.read_csv(edge_path)

    G = nx.DiGraph()    # There should not be duplicate edges that go the same direction.
    # If so, need to throw an error.

    edges = convert_dataframe_to_edges(df)
    add_edges_to_graph(edges, G)
    add_ontology_data_to_graph_nodes(G, onto)
    to_remove = set_edge_properties(G)
    remove_edge_properties_from_nodes(G, to_remove)

    save_graph_to_pickle(G)
    #save_graph_to_gexf(G)
    #save_graph_to_gml(G)
    #save_graph_to_graphml(G)
    # save_graph_to_yaml(G)
    # save_graph_to_json(G)

    valid_test_ont = {
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
        "universalism tolerance"
    }

    not_test_ont = {
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
        "solution uncategorized (to do)"
    }

    get_test_ontology(G, valid_test_ont, not_test_ont)
    #for node in G.nodes:
        #print(node)
        #print(G.nodes[node]["direct classes"])


    save_test_ontology_to_json(G)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='get networkx graph object from ontology after running make_network.py')
    parser.add_argument("refOntologyPath", type=str,
                                            help='path to reference OWL2 ontology')
    parser.add_argument("refEdgeListPath", type=str,
                                            help='path for csv file of result edges (list of object,subject,predicate triples)')
                        
    args = parser.parse_args()
    main(args)

