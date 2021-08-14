from app import db
from flask import jsonify
from flask import make_response
from app.errors import bp
from app.errors.errors import DatabaseError, AlreadyExistsError, CustomError
from flask_cors import cross_origin


@bp.app_errorhandler(CustomError)
@cross_origin()
def handle_custom_error(error):
    response = jsonify({"error": error.message}), error.status_code
    return response


@bp.app_errorhandler(DatabaseError)
@cross_origin()
def handle_database_error(error):
    db.session.rollback()
    response = jsonify({"error": error.message}), error.status_code
    return response


@bp.app_errorhandler(AlreadyExistsError)
@cross_origin()
def handle_existing_resource_error(error):
    response = (
        jsonify({"error": error.message + " already exists in the database."}),
        error.status_code,
    )
    return response


@bp.app_errorhandler(429)
def ratelimit_handler(e):
    return make_response(jsonify(error="ratelimit exceeded %s" % e.description), 429)
