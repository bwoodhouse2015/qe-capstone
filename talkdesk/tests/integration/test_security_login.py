from fastapi.testclient import TestClient
from app import app

client = TestClient(app) ##Creates a fake user


def test_invalid_login_rejected():

    response = client.post(  ##This is sending a HTTP POST request using API
        "/api/login",
        json={ ##Invalid information being input
            "email": "hacker@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code in [401, 403] ##Expected results that would result in a PASS

    ##This tests authentication log in, "Can an invalid user log in?"

    ##Failures would include results of 200 OK, Application crashes with 500 internal error

    ##The reason this is an integration test because it uses 2 components which is the HTTP request > Fast API routing > Authentication logic > HTTP Response
