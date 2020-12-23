import re

from knowledge_graph import db
from knowledge_graph.models import Sessions


def add_zip_code(zipcode, session_id):
    """
    Zip codes are (optionally) given by the user to localise their feed and show the climate change impacts most relevant to where they live.
    A regular expression is used to check whether the zip code contains 5 digits.
    If the zip code is valid, it is committed to the Sessions model alongside the session_id.
    """
    regex = re.compile(r"(\b\d{5})\b")
    mo = regex.search(zipcode)

    if mo != None:
        try:
            session_id = Sessions.query.filter_by(session_id=session_id)
            session_id.postal_code = int(zipcode)

            db.session.commit()
        except KeyError:
            return KeyError
        except ValueError:
            return ValueError
