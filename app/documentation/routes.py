from app.documentation import bp

from app import auto
from flask_cors import cross_origin

"""

Returns auto-generated API documentation based on the docstrings contained in each
API endpoint.

"""


@bp.route("/documentation")
@cross_origin()
def documentation():
    return auto.html()
