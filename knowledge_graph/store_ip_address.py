from typing import Type

from knowledge_graph import db
from knowledge_graph.models import Sessions


def store_ip_address(ip_address, session_id):
    userSession = Sessions.query.filter_by(session_id=session_id).first()
    userSession.ip_address = ip_address
    db.session.commit()
    return None
