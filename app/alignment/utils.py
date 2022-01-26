import os
from json import load

from app.models import AlignmentScores, UserBJourney, Conversations, Users
from app import db

def build_alignment_scores_response(alignment_scores_uuid):

    (alignment, userB_name, userA_name) = (
        db.session.query(AlignmentScores, Conversations.receiver_name, Users.first_name)
        .join(UserBJourney, UserBJourney.alignment_scores_uuid == AlignmentScores.alignment_scores_uuid)
        .join(Conversations, Conversations.conversation_uuid == UserBJourney.conversation_uuid)
        .join(Users, Users.user_uuid == Conversations.sender_user_uuid)
        .filter(AlignmentScores.alignment_scores_uuid == alignment_scores_uuid)
        .one_or_none()
    )

    value_map = get_value_map()

    alignment_scores = [{"valueName":name, "score":get_alignment_value(alignment, name), "description":value_map[name]} for name in value_map.keys()]
    alignment_scores.sort(key=lambda x:-x["score"])
    top_score = alignment_scores[0]

    response = {
        "overallSimilarityScore": as_percent(alignment.overall_similarity_score),
        "topMatchPercent": top_score["score"],
        "topMatchValue": top_score["valueName"],
        "valueAlignment": alignment_scores,
        "userA": userA_name,
        "userB": userB_name
    }

    return response

def get_alignment_value(alignment, value_name):
    return as_percent(getattr(alignment, value_name + "_alignment"))

def as_percent(number):
    return int(100.0 * number)

def get_value_map():
    try:
        file = os.path.join(
            os.getcwd(), "app/personal_values/static", "value_descriptions.json"
        )
        with open(file) as f:
            value_datas = load(f)
        return {key:value_datas[key]['description'] for key in value_datas.keys()}
    except FileNotFoundError:
        return jsonify({"error": "Value descriptions file not found"}), 404

