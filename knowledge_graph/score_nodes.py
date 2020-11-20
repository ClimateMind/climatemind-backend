import pickle
import numpy
import networkx as nx
import sys
from collections import Counter
from knowledge_graph.make_graph import (
    get_test_ontology,
    get_valid_test_ont,
    get_non_test_ont,
)
import numpy as np

OFFSET = 4  # .edu <- to skip these characters and get the unique IRI

def remove_non_value_database_columns(scores):
    if "_sa_instance_state" in scores.keys():
        del scores["_sa_instance_state"]
    if "session_id" in scores.keys():
        del scores["session_id"]
    if "scores_id" in scores.keys():
        del scores["scores_id"]
    if "user_id" in scores.keys():
        del scores["user_id"]
    return scores


def get_effect_id(node):
    try:
        full_iri = node["iri"]
        pos = full_iri.find("edu") + OFFSET
        return full_iri[pos:]
    except:
        return "No IRI Found"

def get_short_description(node):
    try:
        return node["schema_shortDescription"]
    except:
        return "No short desc available at present"

def get_image_url(node):
    try:
        return node["properties"]["schema_image"][0]
    except:
        # Default image url if image is added
        return "https://yaleclimateconnections.org/wp-content/uploads/2018/04/041718_child_factories.jpg"

def simple_scoring(G, user_scores):
    """Each node contains a list of classes, which include the values associated with
    the node. For the simple scoring, only positively associated values are
    considered. All of the users value scores are > 0, meaning negative relationships
    are not considered.
    """
    climate_effects = []
    
    #could probably move this user_scores_vector to the part of the code outside this function that identifies user's values profile scores
    #then just have the user_scores_vector inputted as the input to the simple_scoring() function instead of user_scores so that the 11 lines below aren't?
    user_scores_vector = [
        user_scores["achievement"], 
        user_scores["benevolence"], 
        user_scores["conformity"], 
        user_scores["hedonism"], 
        user_scores["power"], 
        user_scores["security"], 
        user_scores["self_direction"], 
        user_scores["stimulation"], 
        user_scores["tradition"], 
        user_scores["universalism"]
    ]

    for node in G.nodes:
        if node == "decrease in GDP":
            print(G.nodes[node])
        try:
            set_of_values = G.nodes[node]["personal_values_10"]
            print(set_of_values)
        except:
            set_of_values = None

        if set_of_values:
            #print(G.nodes[node])
<<<<<<< HEAD
            full_iri = G.nodes[node]["iri"]
            pos = full_iri.find("edu") + OFFSET
            effect_id = full_iri[pos:]

            #score = 0
            #for value in set_of_values:
            #    score += user_scores[value]
            #np.dot(np.array(user_scores_vector),np.array(nx.get_node_attributes(G,"personal_values_10")[node]))
            node_values_associations_10 = nx.get_node_attributes(G,"personal_values_10")[node]
            #breakpoint()
            if(any(v is None for v in node_values_associations_10)):
                score = 0 #this would be better if was None instead of 0!
            else:
                score = np.dot(user_scores_vector,node_values_associations_10)

            try:
                desc = G.nodes[node]["schema_shortDescription"]
            except:
                desc = "No short desc available at present"

            try:
                imageUrl = G.nodes[node]["properties"]["schema_image"][0]
                #if imageUrl:
                    #breakpoint()
            except:
                # Default image url if image is added
                imageUrl = "https://yaleclimateconnections.org/wp-content/uploads/2018/04/041718_child_factories.jpg"
=======

            score = 0
            #for value in set_of_values:
            #    score += user_scores[value]
>>>>>>> origin/more-refactoring2

            d = {
                "effectId": get_effect_id(G.nodes[node]),
                "effectTitle": G.nodes[node]["label"],
                "effectDescription": get_short_description(G.nodes[node]),
                "effectScore": score,
                "imageUrl": get_image_url(G.nodes[node]),
            }
            climate_effects.append(d)



    return climate_effects


def get_best_nodes(climate_effects, n):
    """Returns the top n Nodes for a user along with the scores for those nodes.

    Parameters
    ----------
    nodes_with_scores - Dictionary containing NetworkX nodes and Integer scores
    n - Integer to specify # of desired scores
    """
    best_nodes = sorted(climate_effects, key=lambda k: k["effectScore"], reverse=True)[
        :3
    ]
    #try sorting where None values get put at the end... sorted(l, key=lambda x: (x is None, x))
    #see https://stackoverflow.com/questions/18411560/python-sort-list-with-none-at-the-end/18411598
    #mylist.sort(key=lambda x: Min if x is None else x)
    #https://stackoverflow.com/questions/12971631/sorting-list-by-an-attribute-that-can-be-none
    return best_nodes


def get_pickle_file(filename):
    G = nx.read_gpickle(filename)
    return G


def get_user_nodes(user_scores):
    G = get_pickle_file("Climate_Mind_DiGraph.gpickle")

    valid_test_ont = get_valid_test_ont()
    not_test_ont = get_non_test_ont()

    get_test_ontology(G, valid_test_ont, not_test_ont)
    climate_effects = simple_scoring(G, user_scores)
    best_nodes_for_user = get_best_nodes(climate_effects, 3)
    return best_nodes_for_user
