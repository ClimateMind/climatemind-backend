from flask import request, jsonify, make_response
from app.auth import bp
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity

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
    user = db.session.query(Users).filter_by(email=email).one_or_none()
    if not user or not user.check_password(password):
        return jsonify({"error": "Wrong username or password"}), 401
    access_token = create_access_token(identity=user, fresh=True)
    refresh_token = create_refresh_token(identity=user)
    response = make_response(
        jsonify(
            {
                "access_token": access_token,
                "user": {
                    "email": user.email,
                    "user_uuid": user.uuid,
                },
            }
        )
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
    print(refresh_token)
    response = make_response(jsonify(access_token=access_token))
    response.set_cookie("refresh_token", refresh_token, path="/refresh", httponly=True)
    return response


@bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(
        uuid=current_user.uuid,
        email=current_user.email,
    )


@bp.route("/register", methods=["POST"])
def register():
    r = request.get_json(force=True)
    email = r.get("email", None)
    password = r.get("password", None)

    user = Users.find_by_username(email)
    if user:
        return jsonify({"error": "Username already taken"}), 401
    else:
        session_uuid = uuid.uuid4()
        user = Users(email=email, uuid=session_uuid)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    return jsonify({"message": "Succesfully created user"}), 201
