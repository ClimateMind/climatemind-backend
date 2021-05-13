from flask import request, jsonify, make_response
from app.auth import bp
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_cors import cross_origin
from app.subscribe.store_subscription_data import check_email

from app.errors.errors import InvalidUsageError, DatabaseError, UnauthorizedError


from app.models import Users

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

    if not valid_name(full_name):
        raise InvalidUsageError(
            message="Full name must be between 2 and 50 characters."
        )

    if check_email(email) and password_valid(password):
        user = Users.find_by_username(email)
    else:
        raise InvalidUsageError(message="Wrong email or password. Try again.")

    if user:
        raise UnauthorizedError(message="Email already registered")
    else:
        user = add_user_to_db(full_name, email, password)

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
