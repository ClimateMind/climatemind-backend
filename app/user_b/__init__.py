from flask import Blueprint

bp = Blueprint("user_b", __name__)

from app.user_b import routes
