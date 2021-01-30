from app.documentation import bp

from app import auto

"""

Returns auto-generated API documentation based on the docstrings contained in each
API endpoint.

"""


@bp.route("/")
def documentation():
    return "Welcome to Climate Mind"


@bp.route("/documentation")
def documentation():
    return auto.html()
