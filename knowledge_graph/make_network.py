#script to make a network (edge list or python graph object) from our Owl2 ontology

from owlready2 import *
import argparse
import pandas as pd

onto_path = "../../Bx50alKwEALYNmYI0CFzNp.owx"

#function to prepare and assign alias name only from supplying a property object.
#Cleans up label names in the process to by python friendly
#have python convert " " and "/" or any other special characters to "_" in the pythonic naming aliases.
def giveAlias(property_object):
    if property_object.label:
        label_name = property_object.label[0]
        label_name = label_name.replace("/","_or_")
        label_name = label_name.replace(" ","_")
        property_object.python_name = label_name

#give Alias probably could use unit test of its own.

#The ‘python_name’ annotations can also be defined in ontology editors like Protégé, by importing the Owlready ontology (file ‘owlready2/owlready_ontology.owl’ in Owlready2 sources
#https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/traversal/edgedfs.html#edge_dfs
#https://networkx.github.io/documentation/networkx-1.10/_modules/networkx/algorithms/traversal/depth_first_search.html#dfs_labeled_edges


def dfs_labeled_edges(ontology,source=None):
    """Produce edges in a depth-first-search (DFS) labeled by type.

    Parameters
    ----------
    ontology : OWL2 climate mind ontology file

    source : node, optional
       Specify starting node for depth-first search and return edges in
       the component reachable from source.

    Returns
    -------
    edges: generator
       A generator of edges in the depth-first-search labeled with the property relation.

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
    visited = set()
    for start in nodes:
        print(start)
        if start in visited:
            continue
        visited.add(start)
        stack = [(start,iter(start.causes_or_promotes))]
        while stack:
            parent,children = stack[-1]
            try:
                child = next(children)
                if child in visited:
                    yield parent.label[0],child.label[0],"causes_or_promotes"
                else:
                    yield parent.label[0],child.label[0],"causes_or_promotes"
                    visited.add(child)
                    stack.append((child,iter(child.causes_or_promotes)))
            except StopIteration:
                stack.pop()
                visitedClasses = set()
                newStart = ontology.get_parents_of(parent)
                if newStart == []:
                    continue
                else:
                    stackClasses = []
                    for newParent in newStart:
                        if newParent != owl.Thing and newParent in ontology.individuals():
                            stackClasses.append((newParent,iter(newParent.causes_or_promotes)))
                            stackClasses.append((newParent,iter(ontology.get_parents_of(newParent))))
                    while stackClasses:
                        parent2,children2 = stackClasses[-1]
                        visitedClasses.add(parent2) #how do we know that parent2 is a class? it doesn't matter?
                        try:
                            child2 = next(children2)
                            if child2 not in ontology.classes() and child2 != owl.Thing and child2 in ontology.individuals():
                           #child2 is an individual so add it to regular stack
                                yield parent2.label[0],child2.label[0],"causes_or_promotes"
                                if child2 not in visited:
                                    visited.add(child2) #is this needed? or wrong? #what if that child is already visited??? should add code to avoid visiting child2?
                                    stack.append((child2,iter(child2.causes_or_promotes)))
                            elif child2 not in visitedClasses and child2 != owl.Thing and child2 in ontology.classes(): #and not owl.Thing?
                                visitedClasses.add(child2)
                                stackClasses.append((child2,iter(child2.causes_or_promotes)))
                                stackClasses.append((child2,iter(ontology.get_parents_of(child2))))
                        except StopIteration:
                            stackClasses.pop()


#include only solutions that stop the nodes outputted?
 

def searchNode(ontology,textString):
    result = list(dfs_labeled_edges(ontology, ontology.search_one(label=textString)))
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
    properties = list(onto.properties())
    [giveAlias(x) for x in properties]

    #make list of edges along all paths leaving the target node
    edges = searchNode(onto,targetNodeLabel)

    #save output to output Path as csv file. Later can change this to integrate well with API and front-end.
    df = pd.DataFrame([[i[0], i[1], i[2]] for i in edges],columns=['subject', 'object', 'predicate'])
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.max_rows', 500)
    print(df)
    print(df[df.duplicated(keep=False)])   
    #df.to_csv(outputPath, index=False)

def mainFunction(targetNodeLabel, ontoPath):
    """
    Main function to output all edges from a reference node. 
    input:
        targetNodeLabel = reference node in the ontology
        ontoPath = path to where the Climate Minde OWL2 ontology is stored
    output:
        Returns a Pandas dataframe of result edges (columns of subject, object, predicate triples)
    example: make_network.mainFunction(“coal mining”, “./climate_mind_ontology20200322.owl”)
    """
    #load ontology
    onto = get_ontology(ontoPath).load()

    #make pythonic alias names for all the properties 
    properties = list(onto.properties())
    [giveAlias(x) for x in properties]

    #make list of edges along all paths leaving the target node
    edges = searchNode(onto,targetNodeLabel)
    
    #output df for use with API
    df = pd.DataFrame([[i[0], i[1], i[2]] for i in edges],columns=['subject', 'object', 'predicate'])
    return df


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
