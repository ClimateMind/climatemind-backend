import requests
import json

def test_get_questions():
    url = 'http://127.0.0.1:5000/questions'
    resp = requests.get(url)

    # Check we get the correct response
    assert resp.status_code == 200

    # Check we have the correct number of questions in each set
    assert len(resp.json()['SetOne']) == 10
    assert len(resp.json()['SetTwo']) == 10

    # Check answers are returned correctly
    assert resp.json()['Answers'] == {
            "1" : "Not Like Me At All",
            "2" : "Not Like Me",
            "3" : "Little Like Me",
            "4" : "Somewhat Like Me",
            "5" : "Like Me",
            "6" : "Very Much Like Me"
    }

    # Check that the two sets have the same question values
    for question in resp.json()['SetOne']:
        assert question['value'] == resp.json()['SetTwo'][question['id'] - 1]['value']


def test_questions_endpoint_parameters():
    url = 'http://127.0.0.1:5000/questions/'
    parameters = ['admin', 'edit', '1']

    for paramter in parameters:
        resp = requests.get(url + paramter)
        assert resp.status_code == 404
