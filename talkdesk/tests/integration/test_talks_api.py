from fastapi.testclient import TestClient
import app as talkdesk


client = TestClient(talkdesk.app)


def test_get_talks_returns_success():
    response = client.get("/api/talks")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

def test_talks_api_response_contract():
    response = client.get("/api/talks")

    assert response.status_code == 200

    talks = response.json()
    assert len(talks) > 0

    first_talk = talks[0]

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

    assert isinstance(first_talk["id"], int)
    assert isinstance(first_talk["title"], str)
    assert isinstance(first_talk["track"], str)
    assert isinstance(first_talk["status"], str)
    assert isinstance(first_talk["speaker"], dict)

    assert {"id", "name"}.issubset(first_talk["speaker"].keys())