from flask import request, jsonify, make_response
from sqlalchemy import desc
from app.auth import bp
import regex as re
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import unset_jwt_cookies
from flask_cors import cross_origin
from app.subscribe.store_subscription_data import check_email

from app.errors.errors import InvalidUsageError, DatabaseError, UnauthorizedError

from app.models import Users, Scores

from app import db, auto

import uuid

"""
A series of endpoints for authentication.
Valid durations for the access and refresh tokens are specified in config.py
Valid URLS to access the refresh endpoint are specified in app/__init__.py
"""


@bp.route("/login", methods=["POST"])
@cross_origin()
@auto.doc()
def login():
    """
    Logs a user in by parsing a POST request containing user credentials.
    User provides email/password.

    Returns: errors if data is not valid.
    Returns: Access token and refresh token otherwise.
    """
    r = request.get_json(force=True, silent=True)

    if not r:
        raise InvalidUsageError(
            message="Email and password must included in the request body"
        )

    email = r.get("email", None)
    password = r.get("password", None)

    if check_email(email):
        user = db.session.query(Users).filter_by(email=email).one_or_none()
    else:
        raise UnauthorizedError(message="Wrong email or password. Try again.")

    if not user or not password_valid(password) or not user.check_password(password):
        raise UnauthorizedError(message="Wrong email or password. Try again.")

    try:
        scores = (
            db.session.query(Scores)
            .filter_by(user_uuid=user.uuid)
            .order_by(desc("scores_created_timestamp"))
            .first()
        )
    except:
        raise DatabaseError(message="Failed to query scores from the database.")

    if scores:
        session_id = scores.session_uuid
    else:
        session_id = None

    access_token = create_access_token(identity=user, fresh=True)
    refresh_token = create_refresh_token(identity=user)

    response = make_response(
        jsonify(
            {
                "message": "successfully logged in user",
                "access_token": access_token,
                "user": {
                    "full_name": user.full_name,
                    "email": user.email,
                    "user_uuid": user.uuid,
                    "session_id": session_id,
                },
            }
        ),
        200,
    )
    response.set_cookie("refresh_token", refresh_token, path="/refresh", httponly=True)
    return response


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    Creates a refresh token and returns a new access token and refresh token to the user.
    This endpoint can only be accessed by URLs allowed from CORS.
    These URLs are specified in app/__init__.py
    """
    identity = get_jwt_identity()
    user = db.session.query(Users).filter_by(uuid=identity).one_or_none()
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    response = make_response(jsonify(access_token=access_token))
    response.set_cookie("refresh_token", refresh_token, path="/refresh", httponly=True)
    return response


@bp.route("/logout", methods=["POST"])
@cross_origin()
def logout():
    """
    Logs the user out by unsetting the refresh token cook
    """
    response = make_response({"message": "User logged out"})
    unset_jwt_cookies(response)
    return response, 200


@bp.route("/protected", methods=["GET"])
@cross_origin()
@jwt_required()
def protected():
    """
    A temporary test endpoint for accessing a protected resource
    """
    return jsonify(
        full_name=current_user.full_name,
        uuid=current_user.uuid,
        email=current_user.email,
    )


@bp.route("/register", methods=["POST"])
@cross_origin()
def register():
    """
    Registration endpoint

    Takes a full_name, email, and password, validates this data and saves the user into the database.
    The user should automatically be logged in upon successful registration.
    The same email cannot be used for more than one account.
    Users will have to take the quiz before registering, meaning the session-id is linked to scores.

    Returns: Errors if any data is invalid
    Returns: Access Token and Refresh Token otherwise
    """
    r = request.get_json(force=True, silent=True)

    if not r:
        raise InvalidUsageError(
            message="Email and password must included in the request body"
        )

    full_name = r.get("fullname", None)
    email = r.get("email", None)
    password = r.get("password", None)
    session_id = r.get("sessionId", None)

    if not valid_name(full_name):
        raise InvalidUsageError(
            message="Full name must be between 2 and 50 characters."
        )

    if not valid_session_id(session_id):
        raise InvalidUsageError(message="Session ID is not a valid UUID4 format.")

    scores = get_scores(session_id)

    if not check_email(email):
        raise InvalidUsageError(message="The email {} is invalid.".format(email))
    if not password_valid(password):
        raise InvalidUsageError(
            message="Password does not fit the requirements."
            "Password must be between 8-20 characters and contain at least one uppercase letter, one lowercase "
            "letter, one number and one special character."
        )

    user = Users.find_by_username(email)
    if user:
        raise UnauthorizedError(message="Email already registered")
    else:
        user = add_user_to_db(full_name, email, password)

    link_user_to_scores(scores, user.uuid)

    access_token = create_access_token(identity=user, fresh=True)
    refresh_token = create_refresh_token(identity=user)
    response = make_response(
        jsonify(
            {
                "message": "Successfully created user",
                "access_token": access_token,
                "user": {
                    "full_name": user.full_name,
                    "email": user.email,
                    "user_uuid": user.uuid,
                    "session_id": scores.session_uuid,
                },
            }
        ),
        201,
    )
    response.set_cookie("refresh_token", refresh_token, path="/refresh", httponly=True)
    return response


def add_user_to_db(full_name, email, password):
    """
    Adds user to database or throws an error if unable to do so.

    Parameters:
        full_name (str)
        email (str)
        password (str)

    Returns: the user object
    """
    session_uuid = uuid.uuid4()
    user = Users(full_name=full_name, email=email, uuid=session_uuid)
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while adding user to the database."
        )
    return user


def link_user_to_scores(scores, user_uuid):
    """
    If a user has already taken the survey, they will have a session-id and
    a set of scores which should be linked to their new account.

    Parameters:
        scores (database object)
        user_uuid (uuid4 as str)
    """
    try:
        scores.user_uuid = user_uuid
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while querying the scores from the database."
        )


def valid_name(full_name):
    """
    Names must be between 2 and 50 characters.
    """
    if not full_name:
        raise InvalidUsageError(message="Full name is missing")
    return 2 <= len(full_name) <= 50


def password_valid(password):
    """
    Passwords must contain uppercase and lowercase letters, and digits.
    Passwords must be between 8 and 20 characters.
    """
    if not password:
        raise InvalidUsageError(
            message="Email and password must included in the request body"
        )

    conds = [
        lambda s: any(x.isupper() for x in s),
        lambda s: any(x.islower() for x in s),
        lambda s: any(x.isdigit() for x in s),
        lambda s: 8 <= len(s) <= 20,
    ]
    return all(cond(password) for cond in conds)


def valid_session_id(session_id):
    """
    Checks for valid UUID4 format
    xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx

    Parameters: session_id (str)

    Returns: True if valid
    """
    regex = re.compile(
        "^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z",
        re.I,
    )
    match = regex.match(session_id)
    return bool(match)


def get_scores(session_id):
    """
    Validates that a session exists within the DB by checking the scores
    table for the most recent scores associated with the provided session id.

    Users may have multiple session IDs if they retake the quiz, so we need to
    return the most recently created version.

    Parameters:
        session_id (uuid4 as str)

    Returns: Scores entry if exists
    Otherwise throws error
    """
    try:
        scores = (
            db.session.query(Scores)
            .filter_by(session_uuid=session_id)
            .order_by(desc("scores_created_timestamp"))
            .first()
        )
    except:
        raise DatabaseError(
            message="An error occurred while querying the scores from the database."
        )

    if not scores:
        raise InvalidUsageError(
            "Provided session ID is not associated with any quiz scores."
        )

    return scores
