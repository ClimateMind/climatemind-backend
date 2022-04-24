from flask import current_app
from app.alignment.utils import map_associated_personal_values


def filter_effects_by_top_aligned_personal_value(top_aligned_personal_value):
    """
    Creates a list of impacts/effects from the ontology that are positively associated with the top aligned personal
    value between users A and B calculated based on comparison of their quiz results.
    """
    G = current_app.config["G"].copy()
    associated_effects = []
    n = 0

    for node in G.nodes:
        current_node = G.nodes[node]

        if "effect" in current_node["all classes"]:
                            
            associated_personal_values = map_associated_personal_values(current_node["personal_values_10"])
            
            if top_aligned_personal_value in associated_personal_values:
                associated_effects.append(current_node)

    return {"number":len(associated_effects)}


def score_aligned_effects():
    """
    Scales and 
    """
    pass