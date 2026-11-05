from fastapi.testclient import TestClient
from app import app

client = TestClient(app) ## creates a testing session to make requests like get, post, and patch, without opening browsers

def test_search_sql_injection():

    payload = "' OR 1=1 --" ## common SQL attack
    ## 1=1 is always true, meaning WHERE true returns every row, -- means ignore everything after this, it is essentially trying to break the db query by tricking it
    ## the database treats the input as data, not executable SQL.
    response = client.get(
        f"/api/talks/search?q={payload}" ## searches the GET response
    )

    assert response.status_code in [200, 400]
    ##200 is acceptable outcome, meaning the application handles the input
    ##400 is acceptable outcome, meaning the application rejected the sus input creating a 400 bad request
    ##Not acceptable would be 500 internal server errors meaning the application crashed with what was input in SQL

    forbidden_strings = [
        "postgres", ## exposes teh data base being used
        "syntax error", ## attacker can learn the query structure, if they reached the db
        "traceback", ## can reveal files names, code locations, function names,
        "database error" ## could reveal table names, column named and the db structure
    ]

    for item in forbidden_strings: ## test will fail if any of these strings present as it could mean too much information can be given away
        assert item not in response.text.lower()


