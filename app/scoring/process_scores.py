import os
from flask import abort, make_response, jsonify
from app.scoring.store_ip_address import store_ip_address


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
            question_id = value["questionId"]
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

    def process_ip_address(self, request, session_uuid):
        """
        Save a user's IP address information into the database with their session_id.
        Provided credentials are for locally generated database (not production).

        Args:
            request: Request
            session_uuid: UUID4

        Returns: Error and Status Code if they exist, otherwise None
        """

        if (
            os.environ["DATABASE_PARAMS"]
            == "Driver={ODBC Driver 17 for SQL Server};Server=tcp:db,1433;Database=sqldb-web-prod-001;Uid=sa;Pwd=Cl1mat3m1nd!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;"
        ):
            try:
                ip_address = None
                store_ip_address(ip_address, session_uuid)
            except:
                abort(make_response(jsonify(error="Error adding ip address locally"), 500))
        else:
            try:
                unprocessed_ip_address = request.headers.getlist("X-Forwarded-For")
                if len(unprocessed_ip_address) != 0:
                    ip_address = unprocessed_ip_address[0]
                # request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
                else:
                    ip_address = None
                store_ip_address(ip_address, session_uuid)
            except:
                abort(make_response(jsonify(error="Error adding ip address in cloud"), 500))
