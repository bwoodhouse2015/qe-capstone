from fastapi.testclient import TestClient
import app as talkdesk

client = TestClient(talkdesk.app)

def test_search_talk_flow():
    """
    Given talks exist

    When the user searches for a talk

    Then matching talks are returned
    """

    response = client.get(
        "/api/talks/search",
        params={"q": "test"}
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)