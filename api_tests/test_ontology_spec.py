import requests

def test_ontology_search_term_not_found():
    url = "http://127.0.0.1:5000/ontology"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    not_found_term = "query=notasearchterm"

    resp = requests.get(url, params=not_found_term, headers=headers)

    # Check we get the correct response
    assert resp.status_code == 400
    assert resp.text == 'query keyword not found'

def test_ontology_no_query():
    url = "http://127.0.0.1:5000/ontology"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    resp = requests.get(url, headers=headers)

    # Check we get the correct response
    assert resp.status_code == 200
    assert resp.text == "{}"
