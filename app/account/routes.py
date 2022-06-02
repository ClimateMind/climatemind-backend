from flask import request, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app import auto, db
from app.account import bp
from app.account.schemas import UserChangePasswordSchema
from app.account.utils import is_email_valid
from app.common.uuid import uuidType, validate_uuid, check_uuid_in_db
from app.errors.errors import (
    AlreadyExistsError,
    DatabaseError,
    InvalidUsageError,
    UnauthorizedError,
    ForbiddenError,
)
from app.models import Users


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
    # FIXME: move to /user-account PUT
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

    if not is_email_valid(new_email):
        raise InvalidUsageError(
            message="Cannot update email. Email is not formatted correctly."
        )

    if new_email != confirm_email:
        raise InvalidUsageError(
            message="Cannot update email. New email address and confirm new email address do not match."
        )

    if not current_user.check_password(password):
        raise UnauthorizedError(message="Cannot update email. Incorrect password.")

    user = Users.find_by_email(new_email)

    # TODO The already exists error format makes this unclear to read in the code, despite the response being clear. Backend to discuss new strategy.
    if user:
        raise AlreadyExistsError(message="Cannot update email. Email")

    try:
        current_user.user_email = new_email
        db.session.commit()
    except SQLAlchemyError:  # pragma: no cover
        raise DatabaseError(
            message="Something went wrong while trying to update the email in the db."
        )

    response = {"message": "User email successfully updated."}

    return jsonify(response), 200


@bp.route("/user-account", methods=["PUT"])
@cross_origin()
@jwt_required()
def update_user_account():
    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    json_data = request.get_json(force=True, silent=True)
    schema = UserChangePasswordSchema()

    try:
        result_data = schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    if current_user.check_password(result_data["current_password"]):
        current_user.set_password(result_data["new_password"])
        db.session.commit()
    else:
        raise ForbiddenError("Invalid password")

    response = {"message": "User password successfully updated."}
    return jsonify(response), 200
