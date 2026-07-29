import os
from pathlib import Path

import snowflake.connector
from dotenv import load_dotenv


# snowflake_connection.py is inside app/.
# parent.parent therefore points to the project root.
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(ENV_PATH)


def get_snowflake_connection():
    """Create and return a Snowflake connection."""

    required_variables = [
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_WAREHOUSE",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_SCHEMA",
    ]

    missing_variables = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing_variables:
        raise ValueError(
            "Missing environment variables: "
            + ", ".join(missing_variables)
        )

    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    )


def test_connection():
    """Test the connection and print basic Snowflake information."""

    connection = None
    cursor = None

    try:
        print(f"Loading configuration from: {ENV_PATH}")
        print(f".env file exists: {ENV_PATH.exists()}")
        print(f"Account loaded: {os.getenv('SNOWFLAKE_ACCOUNT')}")

        connection = get_snowflake_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                CURRENT_USER(),
                CURRENT_ROLE(),
                CURRENT_WAREHOUSE(),
                CURRENT_DATABASE(),
                CURRENT_SCHEMA()
            """
        )

        result = cursor.fetchone()

        print("Snowflake connection successful!")
        print(f"User: {result[0]}")
        print(f"Role: {result[1]}")
        print(f"Warehouse: {result[2]}")
        print(f"Database: {result[3]}")
        print(f"Schema: {result[4]}")

    except Exception as error:
        print("Snowflake connection failed.")
        print(f"Error type: {type(error).__name__}")
        print(f"Error details: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


if __name__ == "__main__":
    test_connection()