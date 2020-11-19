import argparse

import pandas as pd
from owlready2 import *
from knowledge_graph.network_class import Network


def test_answer():
    assert search_node(get_ontology(onto_path).load()) == []
    # need to add in the answer to this unit test.


# still need to make work for when:
# multiple levels of parents
# mutliple parents
# solutions
# reference(?)

# TODO: remove this code and only have it be in the network_class.py code ? Currently, breaks endpoints though if do this.


def outputEdges(onto_path, output_path, source):
    """
    Function to output all edges from a reference node.

    input:
        onto_path = path to ontology
        output_path = path to save output CSV file of edges
        source = specific ontology node to target (optional). Set to None if no source node is desired and want all ontology nodes used.
    output: Saves a csv file of the list of result edges
        (list of object, subject, predicate triples)
    """
    # load ontology
    onto = get_ontology(onto_path).load()

    # make list of edges along all paths leaving the target node
    node_network = Network(onto, source)
    node_network.dfs_labeled_edges()

    # save output to output Path as csv file. Later can change this to integrate well with API and front-end.
    df = pd.DataFrame(
        node_network.edge_triplets, columns=["subject", "object", "predicate"]
    )
    df = df.drop_duplicates()  # Remove if we fix network_class
    df.to_csv(output_path, index=False)


def main(args):
    """
    Main function to output all edges from a reference node.

    input: args = args from the argument parser for the function
                  (refNode, refOntologyPath, outputPath)
    output: Saves a csv file of the list of result edges
            (list of object, subject, predicate triples)

    example: python3 make_network.py "coal mining" "./climate_mind_ontology20200721.owl" "output.csv"
    """

    # set argument variables
    onto_path = args.refOntologyPath
    output_path = args.outputPath
    source = args.source

    outputEdges(onto_path=onto_path, output_path=output_path, source=source)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="get ontology edge from reference node"
    )
    parser.add_argument(
        "-source",
        type=str,
        help="the node you want to start from in the ontology, if None, it will use entire ontology",
    )
    parser.add_argument(
        "refOntologyPath", type=str, help="path to reference OWL2 ontology"
    )
    parser.add_argument(
        "outputPath",
        type=str,
        help="path for output csv file of result edges (list of object,subject,predicate triples)",
    )

    args = parser.parse_args()
    main(args)
