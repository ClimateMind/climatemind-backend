from flask import Blueprint

bp = Blueprint("documentation", __name__)

from app.documentation import routes
