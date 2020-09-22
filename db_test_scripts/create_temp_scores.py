from knowledge_graph import db
from knowledge_graph.models import Scores

def main():
s = Scores(session_id = 1, security = 4.6, conformity = 3.2, benevolence = 1, tradition = 3.3, universalism = 1.2, self_direction = 1.5, stimulation = .3, hedonism = .4, achievement = 2.0, power = .3)
db.session.add(s)
db.session.commit()