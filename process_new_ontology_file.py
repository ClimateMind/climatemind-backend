#From an input OWL file, process it to make files needed for Climate Mind app production and to run helper scripts like visualize.py. Be sure to run from the "backend" folder (not from "knowledge_graph")

import os
import argparse

def main(args):
    """
        Main function that builds files from OWL file starter file. Saved these files to the knowledge_graph repo (note these added files are ignored by git so they don't end up in github later if they are present during a git push). This function should be run from backend repo folder.
        
        input: args = args from the argument parser for the function (refOntologyPath)
        output: saves all ontology-related files needed and used by scripts for the Climate Mind app and tools to knowledge_graph folder.
        
        example: python3 process_new_ontology_file.py "./climate_mind_ontology20200721.owl"
    """
    cwd = os.getcwd()
    
    #set arguments
    onto_path = args.refOntologyPath
    if(args.output_folder):
        output_path = args.output
    
    parent_dir = os.path.dirname('knowledge_graph')
    knowledge_graph_path = os.path.abspath('knowledge_graph')

    command1 = 'python3 "'+ os.path.join(knowledge_graph_path,'make_network.py') + '" "' + onto_path + '" "output.csv"'
    command2 = 'python3 "'+ os.path.join(knowledge_graph_path,'make_graph.py') + '" "' + onto_path + '" "output.csv"'

    os.system(command1)
    os.system(command2)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='From a new ontology OWL file, process it, and files needed by Climate Mind app and associated scripts like visualize.py. Be sure to run from the "backend" folder (not from "knowledge_graph")')
    parser.add_argument("-output_folder", type=str, help='path to alternative output folder')
    parser.add_argument("refOntologyPath", type=str, help='path to reference OWL2 ontology')
    
    
    args = parser.parse_args()
    main(args)
