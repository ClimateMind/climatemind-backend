import datetime
from datetime import timezone
from app import db
from flask import abort, make_response, jsonify
from app.errors.errors import DatabaseError
from app.models import Scores, Sessions


class ProcessScores:
    def __init__(self, questions):
        self.responses_to_add = 10
        self.num_of_responses = 10
        self.num_of_sets = 2
        self.questions = questions
        self.overall_sum = 0
        self.value_scores = {}
        self.value_id_map = {
            1: "conformity",
            2: "tradition",
            3: "benevolence",
            4: "universalism",
            5: "self-direction",
            6: "stimulation",
            7: "hedonism",
            8: "achievement",
            9: "power",
            10: "security",
        }

    def get_value_scores(self):
        return self.value_scores

    def calculate_scores(self, set_name):
        """
        Creates a dictionary of personal values and scores based on the user's responses.

        Args:
            set_name: Str - Valid options are "SetOne" or "SetTwo"

        Returns: value_scores - A dictionary of personal values and scores
                 overall_avg - overall_sum / num_of_responses

        """
        for value in self.questions[set_name]:

            if set_name == "SetOne":
                question_id = value["questionId"]
            elif set_name == "SetTwo":
                question_id = value["questionId"] - 10

            name = self.value_id_map[question_id]
            score = value["answerId"]

            if set_name == "SetOne":
                self.value_scores[name] = score

            elif set_name == "SetTwo":
                avg_score = (self.value_scores[name] + score) / self.num_of_sets
                self.value_scores[name] = avg_score

            self.overall_sum += score

    def center_scores(self, positivity_constant=3.5):
        """
        User scores need to be non-negative and balanced based on their overall average score.

        Args:
            positivity_constant: Int

        Returns: value_scores

        """
        overall_avg = self.overall_sum / self.num_of_responses
        for value, score in self.value_scores.items():
            centered_score = score - overall_avg + positivity_constant

            self.value_scores[value] = centered_score

    def persist_scores(self, user_uuid):
        """
        Saves user scores and session id into the database

        Args: scores
            scores: A dictionary mapping personal values to user scores

        Returns: An error if one occurs

        """
        try:
            user_session = Sessions(session_uuid=self.value_scores["session-id"])
            db.session.add(user_session)

            user_scores = Scores()
            user_scores.session_uuid = self.value_scores["session-id"]
            user_scores.security = self.value_scores["security"]
            user_scores.conformity = self.value_scores["conformity"]
            user_scores.benevolence = self.value_scores["benevolence"]
            user_scores.tradition = self.value_scores["tradition"]
            user_scores.universalism = self.value_scores["universalism"]
            user_scores.self_direction = self.value_scores["self-direction"]
            user_scores.stimulation = self.value_scores["stimulation"]
            user_scores.hedonism = self.value_scores["hedonism"]
            user_scores.achievement = self.value_scores["achievement"]
            user_scores.power = self.value_scores["power"]
            user_scores.scores_created_timestamp = datetime.datetime.now(timezone.utc)

            if user_uuid:
                user_scores.user_uuid = user_uuid

            db.session.add(user_scores)
            db.session.commit()

        except:
            raise DatabaseError(
                message="An error occurred while trying to save the user's scores to the database."
            )
