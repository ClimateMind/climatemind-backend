import uuid
from datetime import datetime

from flask import request, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from app import db, limiter
from app.account import bp
from app.account.schemas import (
    UserChangePasswordSchema,
    LoggedUserChangePasswordSchema,
    SendPasswordResetLinkSchema,
)
from app.account.utils import is_email_valid, check_password_reset_link_is_valid
from app.common.uuid import uuidType, validate_uuid, check_uuid_in_db
from app.errors.errors import (
    ConflictError,
    DatabaseError,
    InvalidUsageError,
    UnauthorizedError,
    ForbiddenError,
)
from app.models import Users, PasswordResetLink
from app.sendgrid.utils import send_reset_password_email


@bp.route("/quizId", methods=["GET"])
@cross_origin()
@jwt_required()
def current_quizId():
    """
    Returns the current quizId of a logged in user or standard JWT errors if token not available or expired.
    """

    response = {"quizId": current_user.quiz_uuid}

    return jsonify(response), 200


@bp.route("/email", methods=["GET"])
@cross_origin()
@jwt_required()
def current_email():
    """
    Returns the current email address of a logged in user or standard JWT errors if token not available or expired.
    """

    response = {"currentEmail": current_user.user_email}

    return jsonify(response), 200


@bp.route("/email", methods=["PUT"])
@cross_origin()
@jwt_required()
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

    if user:
        raise ConflictError(
            message="Cannot update email. Email already exists in the database."
        )

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
    schema = LoggedUserChangePasswordSchema()

    result_data = schema.load(json_data)

    if current_user.check_password(result_data["current_password"]):
        current_user.set_password(result_data["new_password"])
        db.session.commit()
    else:
        raise ForbiddenError("Invalid password")

    response = {"message": "User password successfully updated."}
    return jsonify(response), 200


@bp.route("/user-account", methods=["DELETE"])
@cross_origin()
@jwt_required()
def delete_user_account():
    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    json_data = request.get_json(force=True, silent=True)
    # schema = LoggedUserChangePasswordSchema()
    schema = LoggedUserDeleteAccountScheme()
    result_data = schema.load(json_data)

    if current_user.check_password(result_data["current_password"]):
        # current_user.set_password(result_data["new_password"])
        # delete account
        current_user.delete_account()
        # TO DO: delete session record
        db.session.commit()

    else:
        raise ForbiddenError("Invalid password")

    response = {"message": "User account deleted."}
    return jsonify(response), 200


@bp.route("/password-reset", methods=["POST"])
@limiter.limit("100/day;50/hour;10/minute;5/second")
def create_and_send_password_reset_link_email():
    """
    Returns HTTP codes
    -------
    200 - whenever email is found or not we send OK in security reason
    422 - email is invalid
    404 - session is not found
    400 - invalid or session uuid format
    """
    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    json_data = request.get_json(force=True, silent=True)
    data = SendPasswordResetLinkSchema().load(json_data)

    user = Users.find_by_email(data["email"])
    if user:
        try:
            password_reset = PasswordResetLink(
                uuid=uuid.uuid4(),
                created=datetime.now(),
                user=user,
                session_uuid=session_uuid,
            )
            db.session.add(password_reset)
            db.session.commit()
        except SQLAlchemyError:  # pragma: no cover
            raise DatabaseError(message="Unable to reset password due to DB error")

        send_reset_password_email(
            data["email"],
            password_reset.reset_url,
            PasswordResetLink.EXPIRE_HOURS_COUNT,
        )

    response = {"message": "OK"}
    return jsonify(response), 200


@bp.route("/password-reset/<password_reset_link_uuid>", methods=["GET"])
@cross_origin()
def check_if_password_reset_link_is_expired_or_used(password_reset_link_uuid):
    """
    Returns HTTP codes
    -------
    200 - is OK
    410 - expired
    422 - input email validation issue
    404 - session or password reset link is not found
    400 - invalid password reset link or session uuid format
    """
    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    check_password_reset_link_is_valid(password_reset_link_uuid)

    response = {"message": "Reset password is ready to be used."}
    return jsonify(response), 200


@bp.route("/password-reset/<password_reset_link_uuid>", methods=["PUT"])
@cross_origin()
def do_password_reset(password_reset_link_uuid):
    """
    Returns HTTP codes
    -------
    200 - done
    410 - password reset link is expired
    422 - validation issue
    404 - session or password reset link is not found
    400 - invalid password reset link or session uuid format
    """
    session_uuid = request.headers.get("X-Session-Id")
    session_uuid = validate_uuid(session_uuid, uuidType.SESSION)
    check_uuid_in_db(session_uuid, uuidType.SESSION)

    password_reset = check_password_reset_link_is_valid(password_reset_link_uuid)

    json_data = request.get_json(force=True, silent=True)
    schema = UserChangePasswordSchema()

    result_data = schema.load(json_data)

    try:
        password_reset.user.set_password(result_data["new_password"])
        password_reset.used = True
        db.session.commit()
    except SQLAlchemyError:
        raise DatabaseError(message="Unable to reset password")

    response = {"message": "User password updated successfully."}
    return jsonify(response), 200
