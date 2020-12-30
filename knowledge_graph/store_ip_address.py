from typing import Type

from knowledge_graph import db
from knowledge_graph.models import Sessions


def store_ip_address(ip_address, session_id):
    userSession = Sessions.query.filter_by(session_id=session_id).first()

    if ip_address:
        ip_address = str(ip_address)

    try:
        userSession.ip_address = ip_address
        db.session.commit()
    except Exception as e:
        print(e)

    return None
