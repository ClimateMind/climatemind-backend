import re

from knowledge_graph import db
from knowledge_graph.models import Sessions

def add_zip_code(zipcode, session_id):
    regex = re.compile(r"(\b\d{5})\b")
    mo = regex.search(zipcode)

    if mo != None:
        try:
            session_id = Sessions.query.filter_by(session_id=session_id)
            session_id.zipcode = zipcode

            db.session.commit()
        except KeyError:
            return KeyError