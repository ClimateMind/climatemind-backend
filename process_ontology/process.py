import os
import ontology_processing.process_new_ontology_file

"""

Imports the climatemind-ontology-processing repo and runs the scripts to quickly process
the climatemind ontology.

"""


onto_path = "../PUT_NEW_OWL_FILE_IN_HERE/Bx50aIKwEALYNmYl0CFzNp.owl"
output_folder_path = os.path.join(os.getcwd(), "../output")
ontology_processing.process_new_ontology_file.processOntology(
    onto_path, output_folder_path
)
