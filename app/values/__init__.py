from flask import Blueprint

bp = Blueprint("values", __name__)

from app.values import routes
