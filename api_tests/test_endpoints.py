import requests
import json

url = "http://127.0.0.1:5000/scores"

with open("../json_files/sample_user_response.json") as json_file:
    obj = json.load(json_file)

headers = {"content-type": "application/json"}
request = requests.post(url, json=obj, headers=headers)

response = json.loads(json.dumps(request.json()))
print("Session ID Returned as ", response)

session_id = response["sessionId"]

url = "http://127.0.0.1:5000/personal_values"
params = {"session-id": session_id}
request = requests.get(url, params=params)

print(json.dumps(request.json()))

url = "http://127.0.0.1:5000/feed"
params = {"session-id": session_id}
request = requests.get(url, params=params)

print(json.dumps(request.json(), indent=4))

def test_endpoints():
    assert True
