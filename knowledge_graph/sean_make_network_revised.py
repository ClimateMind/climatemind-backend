from owlready2 import *
import argparse
import pandas as pd

def add_node(parent, node, visited, to_explore, ontology, result):
    
    if node not in visited and node != owl.Thing:
        visited.add(node)
        to_explore.append((node, iter(node.causes_or_promotes)))
        if node in ontology.individuals():
            result.append((parent.label[0], node.label[0], "causes_or_promotes"))
    
        elif node in ontology.classes():
            to_explore.append((node, iter(ontology.get_parents_of(node)))) 


def dfs_helper(ontology, nodes, result, visited, to_explore):
    """Recursive function to produce edges in a depth-first-search (DFS) labeled by type.

    Parameters
    ----------
    ontology : OWL2 climate mind ontology file

    nodes : list of nodes in the ontology
    
    result: A generator of edges in the depth-first-search 
            labeled with the property relation.
    
    visited: A list of already explored nodes
    
    to_explore: A list of nodes still needing exploration
    
           
    """
    if nodes:
        for node in nodes:   
            if node not in visited:
                if node in ontology.individuals():
                    to_explore.append((node, iter(node.causes_or_promotes)))
                if node in ontology.classes():
                    to_explore.append((node, iter(ontology.get_parents_of(node))))
                while to_explore:
                    parent, children = to_explore.pop()
        
                    try:
                        child = next(children)
                        if child.label:
                            result.append((parent.label[0], 
                                            child.label[0], 
                                            "causes_or_promotes"))
                            add_node(parent, child, visited, to_explore, ontology, result)
                
                    except StopIteration:
                        parents = ontology.get_parents_of(node)
                        dfs_helper(ontology, parents, result, visited, to_explore)


def dfs_labeled_edges(ontology, source=None):
    """Initializes a depth-first-search by calling on dfs_helper.

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
        
    if source:
        nodes = [source]
    else:
        nodes = ontology.individuals()

    result = []
    visited = set()
    parents_and_children = []
    
    dfs_helper(ontology, nodes, result, visited, parents_and_children)
    return result

def search_node(ontology,textString):
    return dfs_labeled_edges(ontology, textString)

def test_answer():
    assert search_node(get_ontology(onto_path).load(),"coal mining") == []
    #need to add in the answer to this unit test.


def giveAlias(property_object):
    if property_object.label:
        label_name = property_object.label[0]
        label_name = label_name.replace("/","_or_")
        label_name = label_name.replace(" ","_")
        property_object.python_name = label_name
        

def main(args):
    #set argument variables
    onto_path = args.refOntologyPath
    target_node_label = args.refNode
    output_path = args.outputPath
    
    
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, onto_path)
    
    #load ontology
    onto = get_ontology(filename).load()
    
    #make pythonic alias names for all the properties 
    properties = list(onto.properties())
    [giveAlias(x) for x in properties]

    #make list of edges along all paths leaving the target node
    edges = search_node(onto, None)
    
    #save output to output Path as csv file. Later can change this to integrate well with API and front-end.
    df = pd.DataFrame([[i[0], i[1], i[2]] for i in edges],columns=['subject', 'object', 'predicate'])
    df.to_csv(output_path, index=False)
    

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
