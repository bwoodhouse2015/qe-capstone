from fastapi.testclient import TestClient ##Allows you to send HTTP responses without opening a real browser

from app import app ##imports FastAPI from appy.py

client = TestClient(app) ##Creates a fake user



def test_get_talks_returns_success():
    response = client.get("/api/talks") ##Sends GET response

    assert response.status_code == 200 ##Vaildate status code expected, 200 OK is a pass

    ##Errors 400, 403, 500 will result in fails

    data = response.json() ##This converts JSON into python objects

    assert isinstance(data, list) ## the API returned a list
    assert len(data) > 0 ## Verifies the data exist, at least one talk exists

def test_talks_api_response_contract():
    response = client.get("/api/talks") ##This sends an HTTP GET response

    assert response.status_code == 200 ##Error 200 Ok is expected for a Pass

    talks = response.json()
    assert len(talks) > 0 ##Verifies that there is one record and it is not empty

    first_talk = talks[0] ##This selects the first record as 0 is recognized at the first record in python


##these are the required fields and every talk must contain these
    required_fields = {
        "id",
        "title",
        "track",
        "status",
        "score",
        "speaker",
        "created_at",
    }

    assert required_fields.issubset(first_talk.keys())

    assert isinstance(first_talk["id"], int) ##Verifies an ID is an integer(num)
    assert isinstance(first_talk["title"], str) ##Verifies the title is a string
    assert isinstance(first_talk["track"], str) ##Verifies the track is a string
    assert isinstance(first_talk["status"], str) ##Verifies the status is a string
    assert isinstance(first_talk["speaker"], dict) ##Verifies that the speaker is an object

    assert {"id", "name"}.issubset(first_talk["speaker"].keys()) ##This checks is speaker object contains id and name
