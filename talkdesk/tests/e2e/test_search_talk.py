from fastapi.testclient import TestClient ## Interacts with browser

from app import app ## Imports objects from app.py

client = TestClient(app) ## This creates a simulated user

def test_search_talk_flow():

    response = client.get( ## HTTP GET response
        "/api/talks/search", ## Search end point
        params={"q": "test"} ## Query parameter, adds "?q=test" on the URL which would look like "GET /api/talks/search?q=test"
    )

    assert response.status_code == 200 ## 200 OK is PASS, all other 400, 403, and 500 are failures

    data = response.json() ## This is the returns of the API, converts JSON to python

    assert isinstance(data, list) ## Type validation, did the API return the list?


## Verify the search endpoint accepts a query and returns results in the expected format
