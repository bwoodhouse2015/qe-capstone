import os
import time
import uuid
import psycopg


def test_database_health_and_performance():

    db_url = os.getenv(
        "DB_URL",
        "postgresql://talkdesk:talkdesk@localhost:5432/talkdesk"
    )

    # Measure connection speed
    connection_start = time.perf_counter()

    conn = psycopg.connect(
        db_url,
        connect_timeout=5
    )

    connection_time = time.perf_counter() - connection_start

    with conn:
        with conn.cursor() as cur:

            unique_value = str(uuid.uuid4())

            # Measure write speed
            write_start = time.perf_counter()

            cur.execute("""
                CREATE TEMP TABLE IF NOT EXISTS test_connection (
                    value TEXT
                )
            """)

            cur.execute(
                "INSERT INTO test_connection(value) VALUES (%s)",
                (unique_value,)
            )

            write_time = time.perf_counter() - write_start

            # Measure read speed
            read_start = time.perf_counter()

            cur.execute(
                "SELECT value FROM test_connection WHERE value=%s",
                (unique_value,)
            )

            result = cur.fetchone()

            read_time = time.perf_counter() - read_start

    print(f"\nConnection: {connection_time:.4f}s")
    print(f"Write:      {write_time:.4f}s")
    print(f"Read:       {read_time:.4f}s")

    # Functional validation
    assert result[0] == unique_value

    # Performance thresholds
    assert write_time < 0.5
    assert read_time < 0.5


##this tests is database connect, write and reads?
