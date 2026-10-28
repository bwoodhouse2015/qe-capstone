import os ##imports pythons operating system module
import time ## gives access to start a stop watch
import uuid ##generates unique identifiers
import psycopg ##PostgreSQL driver, connects the test to SQL database


def test_database_health_and_performance():

    db_url = os.getenv(   ##Reads the environment variables, uses the import os, checks to make sure the database exists
        "DB_URL",
        "postgresql://talkdesk:talkdesk@localhost:5432/talkdesk" ##uses this if it cannot find DB_URL
    )

    # Measure connection speed
    connection_start = time.perf_counter()

    conn = psycopg.connect(  ##This connects to PostgreSQL
        db_url,
        connect_timeout=5 ##Waits 5 seconds before failing
    )

    connection_time = time.perf_counter() - connection_start  ## This is used as a stop watch, and this is where it starts the timer of the test

    with conn:
        with conn.cursor() as cur: ## Opens the cursor that executes in SQL

            unique_value = str(uuid.uuid4()) ## This generates a unique value


            write_start = time.perf_counter() # Measures write speed, starts it

                ## This creates a table and column in SQL which is automatically deleted using the TEMP TABLE, no clean up is required
            cur.execute("""
                        CREATE
                        TEMP TABLE IF NOT EXISTS test_connection (
                                value TEXT
                            )
                        """)

            cur.execute(
                "INSERT INTO test_connection(value) VALUES (%s)",  ## The reason we use Values (%s) here is because it is a parameterized query which will prevent SQL injection
                (unique_value,)
            )

            write_time = time.perf_counter() - write_start ## Write time is stopped


            read_start = time.perf_counter() ## Starts time for the read time

            cur.execute(
                "SELECT value FROM test_connection WHERE value=%s", ##This pulls the data that was input during the writing
                (unique_value,)
            )

            result = cur.fetchone() ##This is the stored results in SQL

            read_time = time.perf_counter() - read_start ##Read time has stopped

    print(f"\nConnection: {connection_time:.4f}s") ## This will print out the time of how long it took to connect to SQL
    print(f"Write:      {write_time:.4f}s") ## This will print out the time that is executed for the write time
    print(f"Read:       {read_time:.4f}s") ## This will print out the time that is executed for the read time

    ## Functional validation, this is proving that the data was written > stored correctly > read correctly > matches original value and if the value changes it will result in a fail
    assert result[0] == unique_value

    # Performance thresholds
    assert write_time < 0.5 ## Write must be under 500ms
    assert read_time < 0.5 ## Read must be under 500ms


##this tests is database connect, write and reads? Can my application connect to PostgreSQL, write data, read that same data, and do it in an acceptable amount of time?
##Combination of integration, database, and performance testing.
## Pytest > Python code > Psycopg driver > PostgreSQL server > SQL engine > Resturned data
