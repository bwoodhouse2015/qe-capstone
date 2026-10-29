from fastapi.testclient import TestClient
from app import app

client = TestClient(app) ## Creates user


def test_search_handles_large_input():

    payload = "A" * 10000 ##creates huge string of 10000 A's (characters).

    response = client.get(
        f"/api/talks/search?q={payload}" ##sends it to search endpoint, which is API GET response
    )

    assert response.status_code in [200, 400, 413]

    ##200 OK would be that it has passed, which would mean that the characters were not accepted
    ##400 bad request would be acceptable as it would mean that the characters were not accepted
    ##413 pay load too large would also be an acceptable response

    ##500 error would mean the data input crashed the program, which would result in a failure

    forbidden_strings = [
        "traceback",
        "exception",
        "postgres",
        "syntax error",
        "database error"
    ]

    for item in forbidden_strings:
        assert item not in response.text.lower()


##this tests verifies the program does not crash with invalid characters limit boundaries
