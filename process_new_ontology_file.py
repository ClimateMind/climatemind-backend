# From an input OWL file, process it to make files needed for Climate Mind app production and to run helper scripts like visualize.py. Be sure to run from the "backend" folder (not from "knowledge_graph")

import os
import argparse
from knowledge_graph import app
import knowledge_graph.make_network
import knowledge_graph.make_graph
from network_x_tools.network_x_processor import network_x_processor


def newest(path):
    """
    Return the newest file in a folder. Returns None if there's no file

    Input: folder path
    Output: newest file in folder or None
    """
    files = os.listdir(path)
    paths = [
        os.path.join(path, basename) for basename in files if basename.endswith("owl")
    ]
    if paths:
        newest_path = max(paths, key=os.path.getctime)
    else:
        newest_path = None
    return newest_path


def processOntology(onto_path, output_folder_path):
    """
    Main function that builds files from OWL file starter file. Saved these files to the knowledge_graph repo (note these added files are ignored by git so they don't end up in github later if they are present during a git push). This function should be run from backend repo folder.

    input: args = args from the argument parser for the function (refOntologyPath)
    output: saves all ontology-related files needed and used by scripts for the Climate Mind app and tools to knowledge_graph folder.

    example: python3 process_new_ontology_file.py "./climate_mind_ontology20200721.owl"
    """
    # build output path
    csv_path = os.path.join(output_folder_path, "output.csv")

    # get the network edges from the OWL ontology object
    knowledge_graph.make_network.outputEdges(
        onto_path=onto_path, output_path=csv_path, source=None
    )

    # from the network edges, make a networkx graph and save as a pickle file
    knowledge_graph.make_graph.makeGraph(onto_path, csv_path, output_folder_path)


def main(args):
    """
    Main function that builds files from OWL file starter file. Saved these files to the knowledge_graph repo (note these added files are ignored by git so they don't end up in github later if they are present during a git push). This function should be run from backend repo folder.

    input: args = args from the argument parser for the function (refOntologyPath)
    output: saves all ontology-related files needed and used by scripts for the Climate Mind app and tools to knowledge_graph folder.

    example: python3 process_new_ontology_file.py "./climate_mind_ontology20200721.owl"
    """
    # set arguments
    current_directory = os.getcwd()

    output_folder_path = os.getcwd()
    if args.output_folder:
        output_folder_path = args.output

    base_ontology_path = os.path.join(current_directory, "climate_mind_ontology")

    # if there is a file in the folder PUT_NEW_OWL_FILE_IN_HERE then use that file path as the onto_path, otherwise use the path to the climate_mind_ontology default testing ontology path.
    newest_file_path = newest(
        os.path.join(current_directory, "PUT_NEW_OWL_FILE_IN_HERE")
    )
    if newest_file_path:
        onto_path = newest_file_path
    else:
        onto_path = base_ontology_path

    # process the OWL ontology file
    processOntology(onto_path=onto_path, output_folder_path=output_folder_path)

    try:
        nx_processor = network_x_processor()
    except:
        raise FileNotFoundError("Pickle File Failed to Load as Config Variable")
    try:
        app.config["G"] = nx_processor.get_graph()
    except:
        raise ValidationError("Unable to Load Graph")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='From a new ontology OWL file, process it, and files needed by Climate Mind app and associated scripts like visualize.py. Be sure to run from the "backend" folder (not from "knowledge_graph")'
    )
    parser.add_argument(
        "-output_folder", type=str, help="path to alternative output folder"
    )

    # parser.add_argument("refOntologyPath", type=str, help='path to reference OWL2 ontology')

    args = parser.parse_args()
    main(args)
