import argparse
import pandas as pd
from network_class import Network
from owlready2 import *

def get_edges(ontology):
    node_network = Network(ontology)
    node_network.dfs_labeled_edges()
    return node_network.get_results()


def test_answer():
    assert search_node(get_ontology(onto_path).load()) == []
    #need to add in the answer to this unit test.

#still need to make work for when:
#multiple levels of parents
#mutliple parents
#solutions
#reference(?)

def give_alias(property_object):
    label_name = property_object.label[0]
    label_name = label_name.replace("/","_or_")
    label_name = label_name.replace(" ","_")
    label_name = label_name.replace(":","_")
    property_object.python_name = label_name

def main(args):
    """
    Main function to output all edges from a reference node. 
    input:
        args = args from the argument parser for the function (refNode, refOntologyPath, outputPath)
    output:
        Saves a csv file of the list of result edges (list of object, subject, predicate triples)
    example: python3 make_network.py "coal mining" "./climate_mind_ontology20200721.owl" "output.csv"
    """
    
    #set argument variables
    onto_path = args.refOntologyPath
    output_path = args.outputPath
    
    #load ontology
    onto = get_ontology(onto_path).load()

    #make pythonic alias names for all the properties 
    obj_properties = list(onto.object_properties())
    [give_alias(x) for x in obj_properties]
    annot_properties = list(onto.annotation_properties())
    [give_alias(x) for x in annot_properties]
    

    #make list of edges along all paths leaving the target node
    edges = get_edges(onto)

    #save output to output Path as csv file. Later can change this to integrate well with API and front-end.
    df = pd.DataFrame([[i[0], i[1], i[2]] for i in edges],
                        columns=['subject', 'object', 'predicate'])
    df = df.drop_duplicates() # Remove if we fix network_class
    df.to_csv(output_path, index=False)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='get ontology edge from reference node')
    # parser.add_argument("refNode", type=str,
    #                     help='exact node string that exists in the ontology')
    parser.add_argument("refOntologyPath", type=str,
                        help='path to reference OWL2 ontology')
    parser.add_argument("outputPath", type=str,
                        help='path for output csv file of result edges (list of object,subject,predicate triples)')
    
    args = parser.parse_args()
    main(args)
