import os

import psycopg2


def postgres_client():
    """Creates a connection to the postgres database."""

    conn = psycopg2.connect(
        database=os.getenv("DATABASE"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
        user=os.getenv("USER_NAME"),
        password=os.getenv("PASSWORD"),
        options=f"-c search_path={os.getenv('SCHEMA') or os.getenv('USER_NAME')}",
    )

    return conn.cursor()
