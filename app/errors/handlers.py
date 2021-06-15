from app import db
from flask import jsonify, request
from app.errors import bp
from app.errors.errors import DatabaseError, AlreadyExistsError, CustomError
from flask_cors import cross_origin

import logging
from logging.handlers import SMTPHandler


class EmailErrorFormatter(logging.Formatter):
    def format(self, record):
        record.error_string = str(request.__dict__)
        return super().format(record)


def register_mail_handler(app):
    mail_handler = SMTPHandler(
        mailhost="127.0.0.1",
        fromaddr="server-error@example.com",
        toaddrs=["admin@example.com"],
        subject="Application Error",
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s\n"
            "Request information: %(error_string)"
        )
    )

    app.logger.addHandler(mail_handler)


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
