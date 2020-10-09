import requests
import json

# url = "http://127.0.0.1:5000/scores"
# 
# with open("user_scores_from_nick.json") as json_file:
#     obj = json.load(json_file)
# 
# headers = {"content-type": "application/json"}
# request = requests.post(url, json=obj, headers=headers)
# 
# print(json.dumps(request.json(), indent=4))

url = "http://127.0.0.1:5000/personal_values"
params = {"session-id": "5f5ab575-57d1-4a1b-8b82-08b6b6b1c33e"}
request = requests.get(url, params=params)

print(request.text)

# url = "http://127.0.0.1:5000/get_actions"
#
# with open("sample_user_scores.json") as json_file:
#     obj = json.load(json_file)
#
# headers = {"content-type": "application/json"}
# request = requests.post(url, json=obj, headers=headers)
#
# print(json.dumps(request.json(), indent=4))
#
# url = "http://127.0.0.1:5000/feed"
# params = {"session-id": "6f3225f5-5fd8-4f58-a505-670592e46b9b"}
# request = requests.post(url, params=params)
#
# print(json.dumps(request.json(), indent=4))
