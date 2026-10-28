from fastapi.testclient import TestClient ##Browser control
from pathlib import Path ##used for file system paths, current location of file
import sys ##Specifically for Python runtime settings, controls where python looks for imports

sys.path.insert(0, str(Path(__file__).resolve().parents[2])) ##Uses the import sys

from app import app

client = TestClient(app) ##Creates simulated user


def test_talk_submission_flow():
    print("START TEST") ##This helps identify if a failure occues

    response = client.post( ##Sends a HTTP POST request
        "/api/talks", ##end point responsible for creating the talks
        json={
            "speaker_id": 1,
            "title": "Week 2 E2E Test Talk", ##body converts from python to JSON when sent to APT
            "abstract": "Testing end-to-end submission flow.",
            "track": "testing"
        }
    )

    print("POST FINISHED") ## request is completed

    assert response.status_code == 201 ##status code expected for PASS

    body = response.json() ##API returns this information, converts it back to python

    assert body["title"] == "Week 2 E2E Test Talk" ##Verifies that the API stored the title correctly
    assert body["status"] == "submitted" ##Verifies the new talk was created
