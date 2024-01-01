import os

import pandas as pd
import snowflake.connector

from constants import Databases


def snowflake_client():
    conn = snowflake.connector.connect(
        user=os.getenv("USER_NAME"),
        password=os.getenv("PASSWORD"),
        account=os.getenv("ACCOUNT"),
        warehouse=os.getenv("WAREHOUSE"),
        role=os.getenv("ROLE"),
        database=os.getenv("DATABASE"),
        schema=os.getenv("SCHEMA"),
    )

    # Create a cursor object.
    return conn.cursor()


# function - run sql query and return data
def query_data_warehouse(
    cursor, database_name, sql: str, parameters=None
) -> pd.DataFrame:
    """
    Executes snowflake sql query and returns result as data as dataframe.
    Example of parameters
    :param sql: sql query to be executed
    :param parameters: named parameters used in the sql query (defaulted as None)
    :return: dataframe
    """
    if parameters is None:
        parameters = {}

    try:
        if database_name == Databases.Snowflake.value:
            cursor.execute(f"USE DATABASE {os.getenv('DATABASE')}")
            cursor.execute(f"USE SCHEMA {os.getenv('SCHEMA')}")
        cursor.execute(sql, parameters)
        all_rows = cursor.fetchall()
        field_names = [i[0] for i in cursor.description]

    except snowflake.connector.errors.ProgrammingError as e:
        # print(f"Error in query_data_warehouse: {e}")
        return e

    finally:
        print("closing cursor")

    df = pd.DataFrame(all_rows)
    df.columns = field_names
    return df


def query_table_schema(cursor, database_name, file_path):
    list_table_query = f"""SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{os.getenv('SCHEMA')}'"""
    cursor.execute(list_table_query)
    tables_info = cursor.fetchall()
    tables = [row[0] for row in tables_info]
    table_schema = ""

    for i, table_name in enumerate(tables):
        if database_name == Databases.Snowflake.value:
            table_schema_info = query_data_warehouse(
                cursor, database_name, f"DESCRIBE TABLE {table_name}"
            )
            table_schema = f"**Table {i+1}: {os.getenv('DATABASE')}.{os.getenv('SCHEMA')}.{table_name}**"

        if database_name == Databases.PostgreSQL.value:
            table_schema_info = query_data_warehouse(
                cursor,
                database_name,
                f"SELECT column_name as name, data_type as type FROM information_schema.columns WHERE table_name = '{table_name}'",
            )
            table_schema = f"""**Table {i+1}: "{os.getenv('SCHEMA')}""{table_name}"**"""

        table_schema_info[["name", "type"]].to_csv(
            f"sql/ddl_{table_name.lower()}.csv", index=False
        )

        with open(file_path, "a") as file:
            print("file path", file_path)
            file.write(table_schema + "\n\n")

            for row in table_schema_info.values:
                column_schema = f"- {row[0]}: {row[1]}"
                file.write(column_schema + "\n")

            file.write("\n")
