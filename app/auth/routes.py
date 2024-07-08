from .. import create_app
from app import limiter, db
from app.sendgrid.utils import send_welcome_email
from app.models import Users
from app.errors.errors import (
    ConflictError,
    InvalidUsageError,
    DatabaseError,
    UnauthorizedError,
)
from sqlalchemy.exc import SQLAlchemyError
from app.account.utils import is_email_valid
from flask_jwt_extended import unset_jwt_cookies, get_jwt_identity, create_refresh_token, jwt_required, create_access_token
import requests
from app.common.uuid import validate_uuid, uuidType, check_uuid_in_db
from app.common.local import check_if_local
from app.auth.validators import password_valid
from app.auth import bp
from flask import redirect, request, jsonify, make_response, session, url_for
from datetime import datetime, timezone
import os
import uuid
from app import google_auth

app = create_app()
google = google_auth.init_google_auth(app)
base_frontend_url = app.config['BASE_FRONTEND_URL']


"""
A series of endpoints for authentication.
Valid durations for the access and refresh tokens are specified in config.py
Valid URLS to access the refresh endpoint are specified in app/__init__.py
"""


@limiter.request_filter
def ip_whitelist():
    """
    Adds localhost IP to the rate limiter's whitelist when operating in development environments.
    Prevents conflicts with Cypress testing & VPNs.
    """
    return check_if_local()


@bp.route("/register", methods=["POST"])
@limiter.limit("100/day;50/hour;10/minute;5/second")
def register():
    """
    Registration endpoint

    Takes a first name, last name, email, and password, validates this data and saves the user into the database.
    The user should automatically be logged in upon successful registration.
    The same email cannot be used for more than one account.
    Users will have to take the quiz before registering, meaning the quiz_uuid is linked to scores.

    Returns: Access Token and Refresh Token, or errors if any data is invalid
    """

    r = request.get_json(force=True, silent=True)
    print(r)

    if not r:
        raise InvalidUsageError(
            message="JSON body must be included in the request.")

    for param in ("firstName", "lastName", "email", "password", "quizId"):
        if param not in r:
            raise InvalidUsageError(
                message=f"{param} must be included in the request body."
            )

    quiz_uuid = validate_uuid(r["quizId"], uuidType.QUIZ)
    check_uuid_in_db(quiz_uuid, uuidType.QUIZ)

    for param in ("firstName", "lastName"):
        if not 0 < len(r[param]) <= 20:
            raise InvalidUsageError(
                message=f"{param} cannot be longer than 20 characters."
            )

    if not is_email_valid(r["email"]):
        raise InvalidUsageError(message=f"The email {r['email']} is invalid.")

    if not password_valid(r["password"]):
        raise InvalidUsageError(
            message="Password does not fit the requirements. Password must be between 8-128 characters, contain at least one number or special character, and cannot contain any spaces."
        )

    user = Users.find_by_email(r["email"])
    if user:
        raise ConflictError(
            message="Cannot register email. Email already exists in the database."
        )
    else:
        user = add_user_to_db(
            r["firstName"], r["lastName"], r["email"], r["password"], r["quizId"]
        )

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

    send_welcome_email(user.user_email, user.first_name)

    response.set_cookie("refresh_token", refresh_token,
                        path="/refresh", httponly=True)
    return response


@bp.route("/login", methods=["POST"])
@limiter.limit("100/day;50/hour;10/minute;5/second")
def login():
    """
    Logs a user in by parsing a POST request containing user credentials.
    User provides email/password.

    Returns: Errors if data is not valid or captcha fails.
    Returns: Access token and refresh token otherwise.
    """

    r = request.get_json(force=True, silent=True)

    if not r:
        raise InvalidUsageError(
            message="Email, password and recaptcha must be included in the request body."
        )

    email = r.get("email", None)
    password = r.get("password", None)
    recaptcha_token = r.get("recaptchaToken", None)

    if not password or not email:
        raise InvalidUsageError(
            message="Email and password must be included in the request body."
        )

    user = db.session.query(Users).filter_by(user_email=email).one_or_none()

    if not user or not user.check_password(password):
        raise UnauthorizedError(message="Wrong email or password. Try again.")

    if not check_if_local() and not r.get("skipCaptcha", None):
        # Verify captcha with Google
        secret_key = os.environ.get("RECAPTCHA_SECRET_KEY")

        if not recaptcha_token:
            raise InvalidUsageError(
                message="Recaptcha token must be included in the request body."
            )

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
    response.set_cookie("refresh_token", refresh_token,
                        path="/refresh", httponly=True)
    return response


@bp.route('/register/google')
def register_google():
    quiz_id = request.args.get('quizId')
    session['quiz_id'] = quiz_id
    redirect_uri = url_for('auth.register_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@bp.route('/register/google/callback', methods=['GET'])
def register_callback():
    """
    Finds user by matching google email with user email in the database
    If user doesn't exist, create a new user and add to the database
    Create tokens and set cookies here if needed
    After successful registration, set the user details as cookies and redirect and login user
    """
    try:
        token = google.authorize_access_token()
        resp = google.get('https://www.googleapis.com/oauth2/v3/userinfo')
        user_info = resp.json()
        email = user_info['email']
        quiz_id = session.pop('quiz_id', None)

        if not quiz_id:
            return jsonify({"error": "Quiz ID is missing from session"}), 400

        # find user by matching google email with user email in the database
        user = db.session.query(Users).filter_by(
            user_email=email).one_or_none()

        # if user doesn't exist, create a new user and add to the database
        if not user:
            user = add_user_to_db(
                user_info['given_name'], user_info['family_name'], email, None, quiz_id
            )

        access_token = create_access_token(identity=user, fresh=True)
        refresh_token = create_refresh_token(identity=user)

        response = create_tokens_and_set_cookies(
            user, email, access_token, refresh_token)

        send_welcome_email(user.user_email, user.first_name)
        return response

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "An error occurred while adding user to the database."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/login/google')
def login_google():
    redirect_uri = url_for('auth.callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@bp.route('/login/google/callback', methods=['GET'])
def callback():
    try:
        token = google.authorize_access_token()
        resp = google.get('https://www.googleapis.com/oauth2/v3/userinfo')
        user_info = resp.json()
        email = user_info['email']
        user = db.session.query(Users).filter_by(
            user_email=email).one_or_none()

        if user:
            access_token = create_access_token(identity=user, fresh=True)
            refresh_token = create_refresh_token(identity=user)

            response = create_tokens_and_set_cookies(
                user, email, access_token, refresh_token)
            return response
        else:
            response = make_response(
                redirect(f'{base_frontend_url}/start'))
            return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@limiter.exempt
def refresh():
    """
    Creates a refresh token and returns a new access token and refresh token to the user.
    This endpoint can only be accessed by URLs allowed from CORS.
    These URLs are specified in app/__init__.py

    Returns: A new refresh token and access token.
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
    response.set_cookie("refresh_token", refresh_token,
                        path="/refresh", httponly=True)
    return response


@bp.route("/logout", methods=["POST"])
def logout():
    """
    Logs the user out by unsetting the refresh token cook
    """
    response = make_response({"message": "User logged out"})
    unset_jwt_cookies(response)
    return response, 200


def create_tokens_and_set_cookies(user, email, access_token, refresh_token):
    """
    Creates access and refresh tokens and sets them as cookies.
    Also sets user details as cookies and redirects to a specific URL.

    Parameters:
    - user: User object containing user details (e.g., user.first_name, user.last_name, etc.)
    - email: User's email address
    - access_token: Access token generated for the user
    - refresh_token: Refresh token generated for the user

    Returns:
    - Flask response object with cookies set and redirect
    """
    response = make_response(redirect(
        f'{base_frontend_url}/login?access_token={access_token}&refresh_token={refresh_token}'))
    response.set_cookie("first_name", user.first_name, secure=True)
    response.set_cookie("last_name", user.last_name, secure=True)
    response.set_cookie("user_uuid", user.user_uuid, secure=True)
    response.set_cookie("quiz_id", user.quiz_uuid, secure=True)
    response.set_cookie("user_email", email, secure=True)
    response.set_cookie("refresh_token", refresh_token,
                        path="/refresh", httponly=True)
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

    Returns: The user object
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
    if password:
        user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()

    except SQLAlchemyError:
        raise DatabaseError(
            message="An error occurred while adding user to the database."
        )

    return user
