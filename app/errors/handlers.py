from flask import jsonify, current_app
from flask import make_response
from flask_cors import cross_origin
from marshmallow import ValidationError

from app import db
from app.errors import bp
from app.errors.errors import (
    DatabaseError,
    ConflictError,
    CustomError,
    NotInDatabaseError,
)


def default_error_response(error: CustomError):
    response = jsonify({"error": error.message}), error.status_code
    current_app.logger.exception(error)
    return response


@bp.app_errorhandler(CustomError)
@cross_origin()
def handle_custom_error(error):
    return default_error_response(error)


@bp.app_errorhandler(DatabaseError)
@cross_origin()
def handle_database_error(error):
    db.session.rollback()
    return default_error_response(error)


@bp.app_errorhandler(NotInDatabaseError)
@cross_origin()
def handle_not_in_db_error(error):
    return default_error_response(error)


@bp.app_errorhandler(ConflictError)
@cross_origin()
def handle_conflict_error(error):
    return default_error_response(error)


@bp.app_errorhandler(429)
def ratelimit_handler(e):
    return make_response(jsonify(error="ratelimit exceeded %s" % e.description), 429)


@bp.app_errorhandler(ValidationError)
@cross_origin()
def handle_custom_error(error):
    return make_response(jsonify({"error": error.messages}), 422)
