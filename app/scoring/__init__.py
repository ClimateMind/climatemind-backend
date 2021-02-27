from flask import Blueprint

bp = Blueprint("scoring", __name__)

from app.scoring import routes
