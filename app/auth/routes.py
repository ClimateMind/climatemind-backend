import os
from datetime import datetime, timezone
from flask import request, jsonify, make_response
from sqlalchemy import desc
from app.auth import bp
import regex as re
import requests
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
@auto.doc()
def login():
    """
    Logs a user in by parsing a POST request containing user credentials.
    User provides email/password.

    Returns: errors if data is not valid or captcha fails.
    Returns: Access token and refresh token otherwise.
    """
    r = request.get_json(force=True, silent=True)

    if not r:
        raise InvalidUsageError(
            message="Email and password must be included in the request body."
        )

    email = r.get("email", None)
    password = r.get("password", None)
    recaptcha_token = r.get("recaptchaToken", None)

    if check_email(email):
        user = db.session.query(Users).filter_by(user_email=email).one_or_none()
    else:
        raise UnauthorizedError(message="Wrong email or password. Try again.")

    if not user or not password_valid(password) or not user.check_password(password):
        raise UnauthorizedError(message="Wrong email or password. Try again.")

    # Verify captcha with Google
    secret_key = os.environ.get("RECAPTCHA_SECRET_KEY")
    data = {"secret": secret_key, "response": recaptcha_token}
    resp = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", data=data
    ).json()

    # Google will return True/False in the success field, resp must be json to properly access
    if not resp["success"]:
        raise UnauthorizedError(message="Captcha did not succeed.")

    access_token = create_access_token(identity=user, fresh=True)
    refresh_token = create_refresh_token(identity=user)

    response = make_response(
        jsonify(
            {
                "message": "successfully logged in user",
                "access_token": access_token,
                "user": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.user_email,
                    "user_uuid": user.user_uuid,
                    "quiz_id": user.quiz_uuid,
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
    user = db.session.query(Users).filter_by(user_uuid=identity).one_or_none()
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)

    response = make_response(
        jsonify(
            {
                "message": "successfully refreshed token",
                "access_token": access_token,
                "user": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.user_email,
                    "user_uuid": user.user_uuid,
                    "quiz_id": user.quiz_uuid,
                },
            }
        ),
        200,
    )
    response.set_cookie("refresh_token", refresh_token, path="/refresh", httponly=True)
    return response


@bp.route("/logout", methods=["POST"])
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
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        uuid=current_user.user_uuid,
        email=current_user.user_email,
    )


@bp.route("/register", methods=["POST"])
def register():
    """
    Registration endpoint

    Takes a first name, last name, email, and password, validates this data and saves the user into the database.
    The user should automatically be logged in upon successful registration.
    The same email cannot be used for more than one account.
    Users will have to take the quiz before registering, meaning the quiz_uuid is linked to scores.

    Returns: Errors if any data is invalid
    Returns: Access Token and Refresh Token otherwise
    """
    r = request.get_json(force=True, silent=True)

    if not r:
        raise InvalidUsageError(
            message="Email and password must be included in the request body."
        )

    first_name = r.get("firstName", None)
    last_name = r.get("lastName", None)
    email = r.get("email", None)
    password = r.get("password", None)
    quiz_uuid = r.get("quizId", None)

    if not valid_name(first_name):
        raise InvalidUsageError(
            message="First name must be between 2 and 50 characters."
        )

    if not valid_name(last_name):
        raise InvalidUsageError(
            message="Last name must be between 2 and 50 characters."
        )

    if not quiz_uuid:
        raise InvalidUsageError(message="Quiz UUID must be included to register.")

    try:
        quiz_uuid = uuid.UUID(quiz_uuid)

    except:
        raise InvalidUsageError(message="Quiz UUID is improperly formatted.")

    if not scores_in_db(quiz_uuid):
        raise DatabaseError(message="Quiz ID is not in the db.")

    if not check_email(email):
        raise InvalidUsageError(message=f"The email {email} is invalid.")

    if not password_valid(password):
        raise InvalidUsageError(
            message="Password does not fit the requirements. "
            "Password must be between 8-128 characters, contain at least one number or special character, and cannot contain any spaces."
        )

    user = Users.find_by_username(email)
    if user:
        raise UnauthorizedError(message="Email already registered")
    else:
        user = add_user_to_db(first_name, last_name, email, password, quiz_uuid)

    access_token = create_access_token(identity=user, fresh=True)
    refresh_token = create_refresh_token(identity=user)
    response = make_response(
        jsonify(
            {
                "message": "Successfully created user",
                "access_token": access_token,
                "user": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.user_email,
                    "user_uuid": user.user_uuid,
                    "quiz_id": user.quiz_uuid,
                },
            }
        ),
        201,
    )
    response.set_cookie("refresh_token", refresh_token, path="/refresh", httponly=True)
    return response


def add_user_to_db(first_name, last_name, email, password, quiz_uuid):
    """
    Adds user to database or throws an error if unable to do so.

    Parameters:
        first_name (str)
        last_name (str)
        email (str)
        password (str)
        quiz_uuid (uuid)

    Returns: the user object
    """
    user_uuid = uuid.uuid4()
    user_created_timestamp = datetime.now(timezone.utc)
    user = Users(
        user_uuid=user_uuid,
        first_name=first_name,
        last_name=last_name,
        user_email=email,
        quiz_uuid=quiz_uuid,
        user_created_timestamp=user_created_timestamp,
    )
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while adding user to the database."
        )
    return user


def valid_name(name):
    """
    Names must be between 2 and 50 characters.
    """
    if not name:
        raise InvalidUsageError(message="Name is missing.")
    return 2 <= len(name) <= 50


def password_valid(password):
    """
    Passwords must contain at least one digit or special character.
    Passwords must be between 8 and 128 characters.
    Passwords cannot contain spaces.
    """
    if not password:
        raise InvalidUsageError(
            message="Email and password must be included in the request body."
        )

    conds = [
        lambda s: any(x.isdigit() or not x.isalnum() for x in s),
        lambda s: all(not x.isspace() for x in s),
        lambda s: 8 <= len(s) <= 128,
    ]
    return all(cond(password) for cond in conds)


def scores_in_db(quiz_uuid):
    """
    Check that the quizId received from the frontend is in the scores table in the db.
    """
    scores = db.session.query(Scores).filter_by(quiz_uuid=quiz_uuid).first()
    if scores:
        return True
    else:
        return False
