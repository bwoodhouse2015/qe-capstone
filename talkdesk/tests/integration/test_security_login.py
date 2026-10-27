from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_invalid_login_rejected():

    response = client.post(
        "/api/login",
        json={
            "email": "hacker@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code in [401, 403]
