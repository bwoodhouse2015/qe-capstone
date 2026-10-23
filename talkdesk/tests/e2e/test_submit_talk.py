from fastapi.testclient import TestClient
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app import app

client = TestClient(app)


def test_talk_submission_flow():
    print("START TEST")

    response = client.post(
        "/api/talks",
        json={
            "speaker_id": 1,
            "title": "Week 2 E2E Test Talk",
            "abstract": "Testing end-to-end submission flow.",
            "track": "testing"
        }
    )

    print("POST FINISHED")

    assert response.status_code == 201

    body = response.json()

    assert body["title"] == "Week 2 E2E Test Talk"
    assert body["status"] == "submitted"
