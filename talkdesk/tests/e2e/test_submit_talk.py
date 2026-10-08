from fastapi.testclient import TestClient
import app as talkdesk

client = TestClient(talkdesk.app)

def test_talk_submission_flow():
    """
    Given a speaker is on the submission page

    When valid talk information is submitted

    Then the talk is stored successfully
    """

    response = client.post(
        "/api/talks",
        json={
            "speaker_id": 1,
            "title": "Week 2 E2E Test Talk",
            "abstract": "Testing end-to-end submission flow.",
            "track": "testing"
        }
    )

    assert response.status_code == 201

    body = response.json()

    assert body["title"] == "Week 2 E2E Test Talk"
    assert body["status"] == "submitted"