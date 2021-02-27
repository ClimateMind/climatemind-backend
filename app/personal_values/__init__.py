from flask import Blueprint

bp = Blueprint("personal_values", __name__)

from app.personal_values import routes
