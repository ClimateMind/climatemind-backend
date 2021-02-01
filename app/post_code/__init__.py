from flask import Blueprint

bp = Blueprint("post_code", __name__)

from app.post_code import routes
