from flask import Blueprint

bp = Blueprint("solutions", __name__)

from app.solutions import routes
