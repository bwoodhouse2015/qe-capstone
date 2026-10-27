from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_search_sql_injection():

    payload = "' OR 1=1 --" ## common SQL attack

    response = client.get(
        f"/api/talks/search?q={payload}" ## searchs the GET response
    )

    assert response.status_code in [200, 400]

    ##200 is acceptable outcome, meaning the application handles the input
    ##400 is acceptable outcome, meaning the application rejected the sus input creating a 400 bad request
    ##Not acceptable would be 500 internal server errors meaning the application crashed with what was input in SQL

    forbidden_strings = [
        "postgres",
        "syntax error",
        "traceback",
        "database error"
    ]

    for item in forbidden_strings:
        assert item not in response.text.lower()

##this test created to see if an attacker can break the application using malicious input
