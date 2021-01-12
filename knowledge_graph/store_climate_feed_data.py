from knowledge_graph import db
from knowledge_graph.models import ClimateFeed
import datetime
from datetime import timezone


def store_climate_feed_data(session_id, feed):
    try:
        for i in range(len(feed)):
            effect = ClimateFeed()
            effect.session_id = session_id
            dt = datetime.datetime.now(timezone.utc)
            effect.event_ts = dt
            effect.effect_position = i + 1
            effect.effect_iri = feed[i]["effectId"]
            effect.effect_score = feed[i]["effectScore"]
            solutions = feed[i]["effectSolutions"]

            for i in range(len(solutions)):
                iri = solutions[i]["iri"]
                column_name = "solution_" + str(i + 1) + "_iri"
                setattr(effect, column_name, iri)

            effect.isPossiblyLocal = feed[i]["isPossiblyLocal"]

            db.session.add(effect)
            db.session.commit()
    except Exception as e:
        print(e)
