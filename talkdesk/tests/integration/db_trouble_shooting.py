import os ##imports python operating systen
import psycopg ## imports PostgreSQL driver


def test_database_connection():

    db_url = os.getenv( ## Gets database url
        "DB_URL",
        "postgresql://talkdesk:talkdesk@localhost:5432/talkdesk"
    )

    conn = psycopg.connect( ##Opens connection to database
        db_url,
        connect_timeout=5 ##Prevents hanging forever, wait 5 seconds and then fail
    )

    with conn:
        with conn.cursor() as cur: ## creates a cursor

            cur.execute("SELECT 1") ##sends select1 to SQL

            result = cur.fetchone() ##Reads result

            assert result[0] == 1 ## Verifies the query returned the expected value


## Purpose of this test: Verify the application can connect to PostgreSQL and execute SQL.
## Helped diagnose database connectivity issues that were causing extremely slow test execution.
