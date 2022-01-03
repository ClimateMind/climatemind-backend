from flask import Blueprint

bp = Blueprint("alignment", __name__)

from app.alignment import routes
