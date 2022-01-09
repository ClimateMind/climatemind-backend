from app.models import AlignmentScores, Users
from app import db

def build_alignment_scores_response(alignment_scores_uuid):

    alignment = (
        db.session.query(AlignmentScores)
        .filter_by(alignment_scores_uuid=alignment_scores_uuid)
        .one_or_none()
    )

    value_names = ["benevolence", "security", "self_direction", "power", "universalism", "achievement", "conformity", "tradition", "hedonism", "stimulation"]

    response = {
        "alignmentScore": [{"valueName":name, "score":str(get_alignment_value_percentage(alignment, name)), "description":"blah blah??"} for name in value_names], # TODO: implement description
        "overallSimilarityScore": alignment.overall_similarity_score,
        "userA": "Albert?", # TODO: implement
        "userB": "Beth?" # TODO: implement
    }

    return response

def get_alignment_value_percentage(alignment, value_name):
    return int(100.0 * getattr(alignment, value_name + "_alignment"))
