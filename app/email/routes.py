from sqlalchemy.exc import SQLAlchemyError
from app.subscribe.store_subscription_data import check_email
from flask import request, jsonify

from app.email import bp
from app.models import Users
from app.errors.errors import (
    AlreadyExistsError,
    DatabaseError,
    InvalidUsageError,
    UnauthorizedError,
)
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

from app import auto, db


@bp.route("/email", methods=["GET"])
@cross_origin()
@jwt_required()
@auto.doc()
def current_email():
    """
    Returns the current email address of a logged in user or standard JWT errors if token not available or expired.
    """

    response = {"currentEmail": current_user.user_email}

    return jsonify(response), 200


@bp.route("/email", methods=["PUT"])
@cross_origin()
@jwt_required()
@auto.doc()
def update_email():
    """
    Updates the user's email address.

    Returns an error if:
    - the user is not logged in or token has expired (standard JWT errors)
    - any parameters are missing from the request
    - the new email address is not in a valid format
    - the new email address does match the address given in the confirmed email address field
    - the new email address is already in the db
    """

    request_body = request.get_json(force=True, silent=True)

    for param in ("newEmail", "confirmEmail", "password"):
        if param not in request_body:
            raise InvalidUsageError(
                message=f"{param} must be included in the request body."
            )

    new_email = request_body["newEmail"]
    confirm_email = request_body["confirmEmail"]
    password = request_body["password"]

    if not check_email(new_email):
        raise InvalidUsageError(
            message="Cannot update email. Email is not formatted correctly."
        )

    if new_email != confirm_email:
        raise InvalidUsageError(
            message="Cannot update email. New email address and confirm new email address do not match."
        )

    user = Users.find_by_email(new_email)

    # TODO The already exists error format makes this unclear to read in the code, despite the response being clear. Backend to discuss new strategy.
    if user:
        raise AlreadyExistsError(message="Cannot update email. Email")

    if not current_user.check_password(password):
        raise UnauthorizedError(message="Cannot update email. Incorrect password.")

    try:
        current_user.user_email = new_email
        db.session.commit()
    except SQLAlchemyError:
        raise DatabaseError(
            message="Something went wrong while trying to update the email in the db."
        )

    response = {"message": "User email successfully updated."}

    return jsonify(response), 200
