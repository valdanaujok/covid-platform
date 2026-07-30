from numpy import rint

from snowflake_connection import get_snowflake_connection


def run_eda():
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    try:
        # Analyze the main COVID table
        cursor.execute(
            """
            SELECT
                COUNT(*) AS ROW_COUNT,
                COUNT(DISTINCT COUNTRY_REGION) AS COUNTRY_COUNT,
                MIN(DATE) AS FIRST_DATE,
                MAX(DATE) AS LAST_DATE
            FROM COVID_PROJECT_DB.ANALYTICS.COVID_GOLD_TABLE
            """
        )

        covid_result = cursor.fetchone()

        print("COVID_GOLD analysis")
        print(f"Number of rows: {covid_result[0]}")
        print(f"Number of countries: {covid_result[1]}")
        print(f"First date: {covid_result[2]}")
        print(f"Last date: {covid_result[3]}")

        # Analyze the vaccine table
        cursor.execute(
            """
            SELECT
                COUNT(*) AS ROW_COUNT,
                COUNT(DISTINCT COUNTRY_REGION) AS COUNTRY_COUNT,
                COUNT(DISTINCT VACCINE) AS VACCINE_COUNT
            FROM COVID_PROJECT_DB.ANALYTICS.COUNTRY_VACCINES
            """
        )

        vaccine_result = cursor.fetchone()

        print("\nCOUNTRY_VACCINES analysis")
        print(f"Number of rows: {vaccine_result[0]}")
        print(f"Number of countries: {vaccine_result[1]}")
        print(f"Number of vaccines: {vaccine_result[2]}")

        cursor.execute(
            """
            SELECT
              COUNT_IF(COUNTRY_REGION IS NULL) AS MISSING_COUNTRY,
              COUNT_IF(DATE IS NULL) AS MISSING_DATE,
              COUNT_IF(CASES IS NULL) AS MISSING_CASES,
              COUNT_IF(DEATHS IS NULL) AS MISSING_DEATHS,
              COUNT_IF(POPULATION IS NULL) AS MISSING_POPULATION
            FROM COVID_PROJECT_DB.ANALYTICS.COVID_GOLD_TABLE
            """
        )

        missing_result = cursor.fetchone()

        print("\nMissing values in COVID_GOLD_TABLE")
        print(f"Missing countries: {missing_result[0]}")
        print(f"Missing dates: {missing_result[1]}")
        print(f"Missing cases: {missing_result[2]}")
        print(f"Missing deaths: {missing_result[3]}")
        print(f"Missing population: {missing_result[4]}")

        # Check duplicate country and date combinations
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT
                    COUNTRY_REGION,
                    DATE
                FROM COVID_PROJECT_DB.ANALYTICS.COVID_GOLD_TABLE
                GROUP BY COUNTRY_REGION, DATE
                HAVING COUNT(*) > 1
            )
            """
        )

        duplicate_result = cursor.fetchone()

        print("\nDuplicate check")
        print(f"Duplicate country-date combinations: {duplicate_result[0]}")

    except Exception as error:
        print("EDA failed.")
        print(error)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    run_eda()