from flask import request, jsonify, make_response
from app.auth import bp
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from app.subscribe.store_subscription_data import check_email

from app.errors.errors import InvalidUsageError, DatabaseError, UnauthorizedError


from app.models import Users

from app import db, auto

import uuid


@bp.route("/login", methods=["POST"])
@auto.doc()
def login():
    """
    Logs a user in by parsing a POST request containing user credentials.
    """
    r = request.get_json(force=True)
    email = r.get("email", None)
    password = r.get("password", None)

    if check_email(email):
        user = db.session.query(Users).filter_by(email=email).one_or_none()
    else:
        raise UnauthorizedError(
            message="Email is improperly formatted. Check your email and try again."
        )

    if not user or not user.check_password(password):
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
        201,
    )
    response.set_cookie("refresh_token", refresh_token, path="/refresh", httponly=True)
    return response


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user = db.session.query(Users).filter_by(uuid=identity).one_or_none()
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    response = make_response(jsonify(access_token=access_token))
    response.set_cookie("refresh_token", refresh_token, path="/refresh", httponly=True)
    return response


@bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(
        full_name=current_user.full_name,
        uuid=current_user.uuid,
        email=current_user.email,
    )


@bp.route("/register", methods=["POST"])
def register():
    r = request.get_json(force=True)
    full_name = r.get("fullname", None)
    email = r.get("email", None)
    password = r.get("password", None)

    if not valid_name(full_name):
        raise InvalidUsageError(
            message="Full name must be between 2 and 50 characters."
        )

    if check_email(email):
        user = Users.find_by_username(email)
    else:
        raise InvalidUsageError(
            message="Email is improperly formatted. Check your email and try again."
        )

    if not password_valid(password):
        raise InvalidUsageError(message="Password is in an invalid format.")

    if user:
        raise InvalidUsageError(message="Email is already registered to an account.")
    else:
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

    access_token = create_access_token(identity=user, fresh=True)
    refresh_token = create_refresh_token(identity=user)
    response = make_response(
        jsonify(
            {
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


def valid_name(full_name):
    if not full_name:
        raise InvalidUsageError(
            message="Full name is missing. Check your name and try again."
        )
    return 2 <= len(full_name) <= 50


def password_valid(password):
    if not password:
        raise InvalidUsageError(
            message="Email is missing. Check your email and try again."
        )

    conds = [
        lambda s: any(x.isupper() for x in s),
        lambda s: any(x.islower() for x in s),
        lambda s: any(x.isdigit() for x in s),
        lambda s: 8 <= len(s) <= 20,
    ]
    return all(cond(password) for cond in conds)
