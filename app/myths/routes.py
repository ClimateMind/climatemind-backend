from flask import current_app, jsonify, request
from app.myths import bp
from app.myths.process_myths import process_myths


MYTH_PROCESSOR = process_myths()

from app import auto


@bp.route("/myths", methods=["GET"])
@auto.doc()
def get_general_myths():
    """
    The front-end needs a general myths list and information to serve to user when
    they click the general myths menu button. General myths are ordered based on
    relevance predicted from users personal values.
    """

    try:
        recommended_general_myths = MYTH_PROCESSOR.get_user_general_myth_nodes()
        climate_general_myths = {"myths": recommended_general_myths}
        return jsonify(climate_general_myths), 200

    except:
        return {"error": "Failed to process myths"}, 500


@bp.route("/myths/<string:iri>", methods=["GET"])
def get_myth_info(iri):
    """
    The front-end needs the ability to pull a single myth and its relevant information
    by providing an IRI (unique identifier for an ontology node).
    Parameter (as GET)
    iri - a unique identifier string
    """
    myth_info = MYTH_PROCESSOR.get_specific_myth_info(iri)

    if myth_info:
        specific_myth_info = {"myth": myth_info}
        return jsonify(specific_myth_info), 200

    else:
        return {"error": "IRI does not exist"}, 400
