from typing import Type

from knowledge_graph import db
from knowledge_graph.models import Scores, Sessions, getSession


def persist_scores(scores: dict) -> Type[KeyError]:
    try:
        db_session = getSession()

        s = Sessions()
        s.session_id = scores["session-id"]

        db_session.add(s)
        db_session.commit()

        s = Scores()
        s.session_id = scores["session-id"]
        s.security = scores["security"]
        s.conformity = scores["conformity"]
        s.benevolence = scores["benevolence"]
        s.tradition = scores["tradition"]
        s.universalism = scores["universalism"]
        s.self_direction = scores["self-direction"]
        s.stimulation = scores["stimulation"]
        s.hedonism = scores["hedonism"]
        s.achievement = scores["achievement"]
        s.power = scores["power"]

        db_session.add(s)
        db_session.commit()

    except KeyError:
        return KeyError
