# From an input OWL file, process it to make files needed for Climate Mind app production and to run helper scripts like visualize.py. Then runs visualize.py. Be sure to run from the "backend" folder (not from "knowledge_graph")

import os
import argparse
import process_new_ontology_file
import knowledge_graph.visualize


def newest(path):
    """
    Return the newest file in a folder. Returns None if there's no file

    Input: folder path
    Output: newest file in folder or None
    """
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    if paths:
        newest_path = max(paths, key=os.path.getctime)
    else:
        newest_path = None
    return newest_path


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

    # build gpickle_path
    gpickle_path = os.path.join(output_folder_path, "Climate_Mind_DiGraph.gpickle")

    # process the OWL ontology file
    process_new_ontology_file.processOntology(
        onto_path=onto_path, output_folder_path=output_folder_path
    )

    # make the dashboard app object to visualize the new ontology graph
    app = knowledge_graph.visualize.visualize(gpickle_path)

    # run the app object to visualize the new ontology graph
    app.run_server(debug=False, host="0.0.0.0", port=8050)


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
