from app import db
from flask import jsonify
from app.errors import bp
from app.errors.errors import DatabaseError, AlreadyExistsError, CustomError


@bp.app_errorhandler(CustomError)
def handle_custom_error(error):
    response = jsonify({"error": error.message}), error.status_code
    return response


@bp.app_errorhandler(DatabaseError)
def handle_database_error(error):
    db.session.rollback()
    response = jsonify({"error": error.message}), error.status_code
    return response


@bp.app_errorhandler(AlreadyExistsError)
def handle_existing_resource_error(error):
    response = (
        jsonify({"error": error.message + " already exists in the database."}),
        error.status_code,
    )
    return response
