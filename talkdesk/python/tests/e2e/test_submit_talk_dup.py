from fastapi.testclient import TestClient
from pathlib import Path
import sys

# Make the project root importable when this test is run directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from talkdesk.python.app import app


client = TestClient(app)

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