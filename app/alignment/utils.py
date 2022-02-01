import os
from json import load
from flask import jsonify, current_app

from app.models import (
    AlignmentScores,
    UserBJourney,
    Conversations,
    Users,
    AlignmentFeed,
)
from app.network_x_tools.network_x_utils import network_x_utils
from app import db


def build_alignment_scores_response(alignment_scores_uuid):
    """
    Deal with database interactions to provide response for GET alignment scores request.

    Parameters
    ==========
    alignment_scores_uuid - (UUID) the unique id for the alignment scores

    Returns
    ==========
    JSON:
    - overall similarity score
    - alignment scores for all values, along with their descriptions
    - top value and score from the alignment scores
    - user a's first name
    - user b's name
    """

    (alignment, userB_name, userA_name) = (
        db.session.query(AlignmentScores, Conversations.receiver_name, Users.first_name)
        .join(
            UserBJourney,
            UserBJourney.alignment_scores_uuid == AlignmentScores.alignment_scores_uuid,
        )
        .join(
            Conversations,
            Conversations.conversation_uuid == UserBJourney.conversation_uuid,
        )
        .join(Users, Users.user_uuid == Conversations.sender_user_uuid)
        .filter(AlignmentScores.alignment_scores_uuid == alignment_scores_uuid)
        .one_or_none()
    )

    value_map = get_value_map()

    alignment_scores = [
        {
            "valueName": name,
            "score": get_alignment_value(alignment, name),
            "description": value_map[name],
        }
        for name in value_map.keys()
    ]
    alignment_scores.sort(key=lambda x: -x["score"])

    response = {
        "overallSimilarityScore": as_percent(alignment.overall_similarity_score),
        "topMatchPercent": alignment.top_match_percent,
        "topMatchValue": alignment.top_match_value,
        "valueAlignment": alignment_scores,
        "userAName": userA_name,
        "userBName": userB_name,
    }

    return response


def get_alignment_value(alignment, value_name):
    """Get the alignment score for the value, as a percentage."""
    return as_percent(getattr(alignment, value_name + "_alignment"))


def as_percent(number):
    """Turn number between 0 and 1 to a percentage."""
    return int(100.0 * number)


def get_value_map():
    """Get a name->description dict for all values."""
    try:
        file = os.path.join(
            os.getcwd(), "app/personal_values/static", "value_descriptions.json"
        )
        with open(file) as f:
            value_datas = load(f)
            breakpoint()
        return {key: value_datas[key]["description"] for key in value_datas.keys()}
    except FileNotFoundError:
        return jsonify({"error": "Value descriptions file not found"}), 404


def build_shared_impacts_response(alignment_scores_uuid):
    """
    Deal with database interactions to provide response for GET shared impacts request.

    Parameters
    ==========
    alignment_scores_uuid - (UUID) the unique id for the alignment scores

    Returns
    ==========
    JSON:
    - the id, shared score, short description, title, image url (if available), and associated
    personal value(s) for each shared impact
    - user a's first name
    - user b's name
    """

    G = current_app.config["G"].copy()
    nx = network_x_utils()

    (alignment_scores, alignment_feed, userB_name, userA_name) = (
        db.session.query(
            AlignmentScores,
            AlignmentFeed,
            Conversations.receiver_name,
            Users.first_name,
        )
        .join(
            UserBJourney,
            UserBJourney.alignment_scores_uuid == AlignmentScores.alignment_scores_uuid,
        )
        .join(
            AlignmentFeed,
            AlignmentFeed.alignment_feed_uuid == UserBJourney.alignment_feed_uuid,
        )
        .join(
            Conversations,
            Conversations.conversation_uuid == UserBJourney.conversation_uuid,
        )
        .join(Users, Users.user_uuid == Conversations.sender_user_uuid)
        .filter(AlignmentScores.alignment_scores_uuid == alignment_scores_uuid)
        .one_or_none()
    )

    climate_effects_iris = [
        alignment_feed.aligned_effect_1_iri,
        alignment_feed.aligned_effect_2_iri,
        alignment_feed.aligned_effect_3_iri,
    ]

    climate_effects_iris = [
        "webprotege.stanford.edu." + iri for iri in climate_effects_iris
    ]

    climate_effects = effect_details(G, climate_effects_iris, nx)

    response = {
        "climateEffects": climate_effects,
        "userAName": userA_name,
        "userBName": userB_name,
    }

    return response


def effect_details(G, climate_effects_iris, nx):
    """Get the full details for each shared climate impact, including id, shared score, description, title, image (if available), and
    associated personal values."""

    climate_effects = []

    # TODO: implement shared scores
    for iri in climate_effects_iris:
        for node in G.nodes:
            if G.nodes[node]["iri"] == iri:
                nx.set_current_node(G.nodes[node])
                effect = {
                    "effectId": nx.get_node_id(),
                    "sharedScore": 42.00,
                    "effectShortDescription": nx.get_short_description(),
                    "effectTitle": G.nodes[node]["label"],
                    "imageUrl": nx.get_image_url_or_none(),
                    "relatedPersonalValues": map_associated_personal_values(
                        G.nodes[node]["personal_values_10"]
                    ),
                }

                climate_effects.append(effect)

    return climate_effects


def get_personal_values_map():
    """Load the data from the schwartz questions JSON file."""

    try:
        file = os.path.join(
            os.getcwd(), "app/questions/static", "schwartz_questions.json"
        )
        with open(file) as json_file:
            data = load(json_file)
    except FileNotFoundError:
        return jsonify({"error": "Schwartz questions not found"}), 404
    return data


def map_associated_personal_values(personal_values_boolean_list):
    """Take the associated personal values for a shared impact and map them to the value names from the schwartz questions JSON file.

    Parameters
    ==========
    - a list of 10 boolean values (0 or 1) taken from the impact's NetworkX node information that indicate whether a climate impact is associated
    with that personal value

    Returns
    ==========
    - a list of personal values associated with a climate impact

    """

    personal_values_map = get_personal_values_map()

    json_value_ids = [8, 3, 1, 7, 9, 10, 5, 6, 2, 4]

    value_dict = dict(zip(json_value_ids, personal_values_boolean_list))

    personal_values = []

    for key, val in value_dict.items():
        if val:
            for value in personal_values_map["SetOne"]:
                if key == value["id"]:
                    personal_values.append(value["value"])

    return personal_values
