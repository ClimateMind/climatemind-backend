import requests
import json

url = 'http://127.0.0.1:5000/users/scores'

with open('sample_user_response.json') as json_file:
    obj = json.load(json_file)

headers = {'content-type' : 'application/json'}
request = requests.post(url, json=obj, headers=headers)

print(json.dumps(request.json(), indent=4))

url = 'http://127.0.0.1:5000/get_actions'

with open('sample_user_scores.json') as json_file:
    obj = json.load(json_file)

headers = {'content-type' : 'application/json'}
request = requests.post(url, json=obj, headers=headers)