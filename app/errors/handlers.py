import app
from app import db
from flask import jsonify, request, current_app
import flask
import json
from app.errors import bp
from app.errors.errors import DatabaseError, AlreadyExistsError, CustomError
from flask_cors import cross_origin

import logging
from logging.handlers import SMTPHandler


class EmailErrorFormatter(logging.Formatter):
    """
    Formats error logs to include request information (e.g. URL, HTTP method)
    Converts the whole `request` dict into string format
    """

    def format(self, record):
        """
        Required method to implement a custom formatter. Inserts request information into the email, so we know
        what URL parameters, body, cookie, ... caused the error.
        """
        if flask.has_request_context():
            record.error_string = json.dumps(
                request.__dict__, indent=4, default=lambda o: f"{str(type(o))}"
            )
        else:
            record.error_string = "Not in request"
        return super().format(record)


def register_mail_handler(app):
    """
    Registers the `app.logger` instance to use another handler at the "Error" log level.
    Will email these log messages via default `SMTPHandler` to admin email.

    app: Flask app instance
    """
    mail_handler = SMTPHandler(
        # Replace mailhost with (addr, port) of correct SMTP server.
        mailhost=("127.0.0.1", 1025),
        fromaddr="climatemind-server@climatemind.org",
        toaddrs=["hello@climatemind.org"],
        subject="Application Error",
    )

    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(
        EmailErrorFormatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s\n"
            "Request information: %(error_string)s"
        )
    )
    app.logger.addHandler(mail_handler)


@bp.app_errorhandler(CustomError)
@cross_origin()
def handle_custom_error(error):
    response = jsonify({"error": error.message}), error.status_code
    current_app.logger.error(error.message)

    return response


@bp.app_errorhandler(DatabaseError)
@cross_origin()
def handle_database_error(error):
    db.session.rollback()
    response = jsonify({"error": error.message}), error.status_code

    current_app.logger.error(error.message)
    return response


@bp.app_errorhandler(AlreadyExistsError)
@cross_origin()
def handle_existing_resource_error(error):
    response = (
        jsonify({"error": error.message + " already exists in the database."}),
        error.status_code,
    )

    current_app.logger.error(error.message)
    return response
