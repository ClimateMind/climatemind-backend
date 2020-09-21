from flask import Flask

import unittest
from knowledge_graph import db
from knowledge_graph.persist_scores import persist_scores
from knowledge_graph.models import Scores


class TestPersistScores(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        db.init_app(self.app)

        Scores.__table__.create(db.session.bind, checkfirst=True)

    def tearDown(self) -> None:
        db.drop_all()

        db.session.commit()

    def test_successful_persisting(self):
        test_data = {
            "session_id": 1,
            "security": 1.0,
            "conformity": 1.0,
            "benevolence": 1.0,
            "tradition": 1.0,
            "universalism": 1.0,
            "self-direction": 1.0,
            "stimulation": 1.0,
            "hedonism": 1.0,
            "achievement": 1.0,
            "power": 1.0
        }

        expected_scores = Scores()
        expected_scores.session_id = test_data["session_id"]
        expected_scores.security = test_data["security"]
        expected_scores.conformity = test_data["conformity"]
        expected_scores.benevolence = test_data["benevolence"]
        expected_scores.tradition = test_data["tradition"]
        expected_scores.universalism = test_data["universalism"]
        expected_scores.self_direction = test_data["self-direction"]
        expected_scores.stimulation = test_data["stimulation"]
        expected_scores.hedonism = test_data["hedonism"]
        expected_scores.achievement = test_data["achievement"]
        expected_scores.power = test_data["power"]

        persist_scores(test_data)

        test_scores = db.session.query(Scores).filter_by(session_id=1).one()

        self.assertEqual(test_scores.session_id, expected_scores.session_id)

        self.tearDown()


if __name__ == '__main__':
    unittest.main()
