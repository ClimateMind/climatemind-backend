# import requests
# import json
# import time
#
#


def test_get_questions():
    assert True


# def test_get_questions():
#     url = "http://127.0.0.1:5000/questions"
#     resp = requests.get(url)
#     # Check we get the correct response
#     assert resp.status_code == 200
#
#     # Check we have the correct number of questions in each set
#     assert len(resp.json()["SetOne"]) == 10
#     assert len(resp.json()["SetTwo"]) == 10
#
#     # Check answers are returned correctly
#     assert resp.json()["Answers"] == [
#         {"id": 1, "text": "Not Like Me At All"},
#         {"id": 2, "text": "Not Like Me"},
#         {"id": 3, "text": "Little Like Me"},
#         {"id": 4, "text": "Somewhat Like Me"},
#         {"id": 5, "text": "Like Me"},
#         {"id": 6, "text": "Very Much Like Me"},
#     ]
#
#     # Check that the two sets have the same question values
#     for question in resp.json()["SetOne"]:
#         assert question["value"] == resp.json()["SetTwo"][question["id"] - 1]["value"]
#
#
# def test_questions_endpoint_parameters():
#     url = "http://127.0.0.1:5000/questions"
#     parameters = ["admin", "edit", "1"]
#
#     for parameter in parameters:
#         resp = requests.get(url + parameter)
#         assert resp.status_code == 500
