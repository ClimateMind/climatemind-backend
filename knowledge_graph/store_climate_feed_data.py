from knowledge_graph import db
from knowledge_graph.models import ClimateFeed
import datetime
from datetime import timezone


def store_climate_feed_data(session_id, feed):
    n = 1
    for card in feed:
        effect = ClimateFeed()
        effect.session_id = session_id
        dt = datetime.datetime.now(timezone.utc)
        effect.event_ts = dt
        effect.effect_position = n
        effect.effect_iri = card["effectId"]
        effect.effect_score = card["effectScore"]
        solutions = card["effectSolutions"]

        i = 1
        for solution in solutions:
            if i == 1:
                effect.solution_1_iri = solution["iri"]
            elif i == 2:
                effect.solution_2_iri = solution["iri"]
            elif i == 3:
                effect.solution_3_iri = solution["iri"]
            else:
                effect.solution_4_iri = solution["iri"]
            i += 1

        effect.isPossiblyLocal = card["isPossiblyLocal"]

        db.session.add(effect)
        db.session.commit()
        n += 1
