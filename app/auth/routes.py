from flask import request, jsonify
from app.auth import bp
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

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
    username = r.get("username", None)
    password = r.get("password", None)
    user = Users.get_user(username)
    if not user or not user.check_password(password):
        return jsonify({"error": "Wrong username or password"}), 401
    access_token = create_access_token(identity=user)
    response = jsonify(
        {
            "access_token": access_token,
            "username": user.username,
            "email": user.email,
            "user_uuid": user.user_uuid,
        }
    )
    set_access_cookies(response, access_token)
    return response


@bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(
        uuid=current_user.user_uuid,
        username=current_user.username,
        email=current_user.email,
    )


@bp.route("/register", methods=["POST"])
def register():
    r = request.get_json(force=True)
    username = r.get("username", None)
    password = r.get("password", None)
    email = r.get("email", None)

    user = Users.get_user(username)
    if user:
        return jsonify({"Error": "Username already taken"}), 401
    else:
        session_uuid = uuid.uuid4()
        user = Users(username=username, email=email, user_uuid=session_uuid)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    return jsonify({"Message": "Succesfully created user"}), 200


@bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response
