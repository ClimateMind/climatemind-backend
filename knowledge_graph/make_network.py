from owlready2 import *
import argparse
import pandas as pd

onto_path = "./climate_mind_ontology20200322.owl"

#function to prepare and assign alias name only from supplying a property object.
#Cleans up label names in the process to by python friendly
#have python convert " " and "/" or any other special characters to "_" in the pythonic naming aliases.
def giveAlias(property_object):
    label_name = property_object.label[0]
    label_name = label_name.replace("/","_or_")
    label_name = label_name.replace(" ","_")
    property_object.python_name = label_name

#give Alias probably could use unit test of its own.

#The ‘python_name’ annotations can also be defined in ontology editors like Protégé, by importing the Owlready ontology (file ‘owlready2/owlready_ontology.owl’ in Owlready2 sources
#https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/traversal/edgedfs.html#edge_dfs
#https://networkx.github.io/documentation/networkx-1.10/_modules/networkx/algorithms/traversal/depth_first_search.html#dfs_labeled_edges


def dfs_for_classes(ontology, parent, visited, stack, result, edge_type):
    visited_classes = set()
    classes = ontology.get_parents_of(parent)
    if classes:
        class_family = []
        for ont_class in classes:
            if ont_class != owl.Thing:
                try:
                    class_family.append((ont_class, iter(getattr(ont_class, edge_type))))
                    class_family.append((ont_class, iter(ontology.get_parents_of(ont_class))))
                except:
                    pass # Restriction objects are causing an error, should investigate more
        while class_family:
            parent2, children2 = class_family[-1]
            visited_classes.add(parent2) #how do we know that parent2 is a class? it doesn't matter?
            
            try:
                child2 = next(children2)
                if child2 != owl.Thing:
                
                    if child2 in ontology.individuals():
                        # Possibly factor this code to -> add_child_to_result, currently causes an error to do that
                        result.append((parent.label[0], child2.label[0], edge_type))
                        if child2 not in visited:
                            visited.add(child2)
                            stack.append((child2,iter(getattr(child2, edge_type))))
                            
                    elif child2 not in visited_classes and child2 in ontology.classes():
                        visited_classes.add(child2)
                        class_family.append((child2,iter(getattr(child2, edge_type))))
                        class_family.append((child2,iter(ontology.get_parents_of(child2))))
                        
            except StopIteration:
                class_family.pop()
                    

def add_child_to_result(child, parent, result, visited, node_family, edge_type):
    result.append((parent.label[0], child.label[0], edge_type))
    if child not in visited:
        visited.add(child)
        node_family.append((child, iter(getattr(child, edge_type))))

    
def dfs_labeled_edges(ontology, edge_type, source=None):
    """Produce edges in a depth-first-search (DFS) labeled by type.
    Parameters
    ----------
    ontology : OWL2 climate mind ontology file
    source : node, optional
       Specify starting node for depth-first search and return edges in
       the component reachable from source.
    Returns
    -------
    result: list of triples (3-tuple)
       A list of edges in the depth-first-search labeled with the property relation.
    Notes
    -----
    Based on http://www.ics.uci.edu/~eppstein/PADS/DFS.py
    by D. Eppstein, July 2004.
    If a source is not specified then a source is chosen arbitrarily and
    repeatedly until all components in the graph are searched.
    """
    # modified from  http://www.ics.uci.edu/~eppstein/PADS/DFS.py
    # by D. Eppstein, July 2004.
    
    if source is None:
        # produce edges for all components
        nodes = ontology.individuals()
    else:
        # produce edges for components with source
        nodes = [source]
    
    result = []
    visited = set()
    
    for node in nodes:
        if node not in visited:
            visited.add(node)
            node_family = [(node, iter(getattr(node, edge_type)))]
            while node_family:
                parent, children = node_family[-1]
                try:
                    child = next(children)
                    add_child_to_result(child, parent, result, visited, node_family, edge_type)
                except StopIteration:
                    node_family.pop()
                    dfs_for_classes(ontology, parent, visited, node_family, result, edge_type)
    return result


#include only solutions that stop the nodes outputted?
 

def searchNode(ontology,textString):
    result = dfs_labeled_edges(ontology, "causes_or_promotes", ontology.search_one(label=textString))
    return result


def test_answer():
    assert searchNode(get_ontology(onto_path).load(),"coal mining") == []
    #need to add in the answer to this unit test.

#still need to make work for when:
#multiple levels of parents
#mutliple parents
#solutions
#reference(?)


def main(args):
    """
    Main function to output all edges from a reference node. 
    input:
        args = args from the argument parser for the function (refNode, refOntologyPath, outputPath)
    output:
        Saves a csv file of the list of result edges (list of object, subject, predicate triples)
    example: python3 make_network.py "coal mining" "./climate_mind_ontology20200322.owl" "output.csv"
    """
    
    #set argument variables
    ontoPath = args.refOntologyPath
    targetNodeLabel = args.refNode
    outputPath = args.outputPath
    
    #load ontology
    onto = get_ontology(ontoPath).load()

    #make pythonic alias names for all the properties 
    properties = list(onto.object_properties())
    [giveAlias(x) for x in properties]

    #make list of edges along all paths leaving the target node
    edges = searchNode(onto,targetNodeLabel)

    #save output to output Path as csv file. Later can change this to integrate well with API and front-end.
    df = pd.DataFrame([[i[0], i[1], i[2]] for i in edges],columns=['subject', 'object', 'predicate'])
    df.to_csv(outputPath, index=False)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='get ontology edge from reference node')
    parser.add_argument("refNode", type=str,
                        help='exact node string that exists in the ontology')
    parser.add_argument("refOntologyPath", type=str,
                        help='path to reference OWL2 ontology')
    parser.add_argument("outputPath", type=str,
                        help='path for output csv file of result edges (list of object,subject,predicate triples)')
    
    args = parser.parse_args()
    main(args)
