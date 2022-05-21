import datetime
import typing
import uuid
from datetime import timezone
from app import db
from flask import abort, make_response, jsonify

from app.personal_values.enums import PersonalValue
from app.errors.errors import DatabaseError
from app.models import Scores, Users


class ProcessScores:
    def __init__(self, questions):
        self.responses_to_add = 10
        self.questions = questions
        self.num_of_sets = len(questions)
        self.num_of_responses = 10 * self.num_of_sets
        self.overall_sum = 0
        self.value_scores = {}

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

            value_type = PersonalValue(question_id)
            score = value["answerId"]

            if set_name == "SetOne":
                self.value_scores[value_type] = score

            elif set_name == "SetTwo":
                avg_score = (self.value_scores[value_type] + score) / self.num_of_sets
                self.value_scores[value_type] = avg_score

            self.overall_sum += score

    def center_scores(self, positivity_constant=6):
        """
        User scores need to be non-negative and balanced based on their overall average score.

        Args:
            positivity_constant: Int

        Returns: value_scores

        """
        overall_avg = self.overall_sum / self.num_of_responses
        for value_type, score in self.value_scores.items():
            centered_score = score - overall_avg + positivity_constant

            self.value_scores[value_type] = centered_score

    def persist_scores(self, user_uuid, session_uuid):
        """
        Saves user scores and session id into the database

        Args: scores
            scores: A dictionary mapping personal values to user scores

        Returns: An error if one occurs

        """
        try:
            user_scores = Scores()
            # FIXME: value_scores["quiz_uuid"] set outside the class
            #  quiz_uuid shouldn't be in this dict at all
            user_scores.quiz_uuid = self.value_scores["quiz_uuid"]
            for v in PersonalValue:
                setattr(user_scores, v.key, self.value_scores[v])
            user_scores.scores_created_timestamp = datetime.datetime.now(timezone.utc)
            user_scores.session_uuid = session_uuid

            if user_uuid:
                user_scores.user_uuid = user_uuid
                user = Users.query.filter_by(user_uuid=user_uuid).first()
                user.quiz_uuid = self.value_scores["quiz_uuid"]

            db.session.add(user_scores)
            db.session.commit()

        except:
            raise DatabaseError(
                message="An error occurred while trying to save the user's scores to the database."
            )


def get_scores_list(quiz_uuid: uuid.UUID) -> typing.List[float]:
    """
    Get a list of a user's quiz scores, ordered alphabetically by personal values.

    Parameters
    ==========
    quiz_uuid (UUID)

    Returns
    ==========
    scores_list - a list of floats
    """
    user_scores = (
        db.session.query(Scores).filter(Scores.quiz_uuid == quiz_uuid).one_or_none()
    )

    scores_list = [getattr(user_scores, v.key) for v in PersonalValue]

    return scores_list


def get_scores_map(scores: Scores) -> dict:
    """Convert a Scores object into a map from personal value names to numerical scores."""
    return {v.key: getattr(scores, v.key) for v in PersonalValue}
