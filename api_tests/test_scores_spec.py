import requests
import json

url = "http://localhost:5000/scores"
headers = {"Accept": "application/json, */*", "Content-Type": "application/json"}


def test_scores_complete_set_one():
    contents = open("api_tests/test_json/ten_answers.json", "rb").read()

    resp = requests.post(url, data=contents, headers=headers)

    # Check we get the correct response
    assert resp.status_code == 201

    # Check that we have a session ID
    assert resp.json()["sessionId"]


def test_scores_incomplete_set_one():
    contents = open("api_tests/test_json/five_answers.json", "rb").read()

    resp = requests.post(url, data=contents, headers=headers)

    # Check we get the correct response
    assert resp.status_code == 400

    # Check we've failed for the correct reason
    assert resp.text == "not enough set one scores"


def test_scores_too_many_answers_in_set_one():
    contents = open("api_tests/test_json/eleven_answers.json", "rb").read()

    resp = requests.post(url, data=contents, headers=headers)

    # Check we get the correct response
    assert resp.status_code == 400

    # Check we've failed for the correct reason
    assert resp.text == "too many set one scores"


# TODO: this currently fails because of https://climatemind.atlassian.net/browse/CM-115
# Once that is fixed we should uncomment this and then expand the tests for two sets
# def test_scores_two_sets_of_answers():
#     contents = open("api_tests/test_json/twenty_answers.json", "rb").read()
#
#     resp = requests.post(url, data=contents, headers=headers)
#
#     # Check we get the correct response
#     assert resp.status_code == 201
#
#     # Check we've failed for the correct reason
#     assert resp.text == "too many set one scores"
