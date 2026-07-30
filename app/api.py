from fastapi import FastAPI, HTTPException
from snowflake_connection import get_snowflake_connection

#
import os
from pathlib import Path

#import for loading environment variables and connecting to MongoDB
from dotenv import load_dotenv
from pymongo import MongoClient

#imports for MongoDB comments endpoint and datetime handling
from datetime import datetime, timezone
from pydantic import BaseModel

# Load settings from the .env file for MongoDB connection
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path, override=True)

mongodb_uri = os.getenv("MONGODB_URI")


# Create the API application
app = FastAPI(
    title="COVID-19 Data API",
    description="API for COVID-19 data and user comments",
)


# Define the comment structure for the MongoDB comments endpoint
class Comment(BaseModel):
    country: str
    comment: str

# Basic endpoint
@app.get("/")
def home():
    return {
        "message": "COVID-19 Data API is working"
    }


# Health-check endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

# Endpoint to get the list of countries
@app.get("/countries")
def get_countries():

    # Connect to Snowflake
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    # Request unique countries
    cursor.execute(
        """
        SELECT DISTINCT COUNTRY_REGION
        FROM COVID_PROJECT_DB.ANALYTICS.COVID_GOLD_TABLE
        WHERE COUNTRY_REGION IS NOT NULL
        ORDER BY COUNTRY_REGION
        """
    )

    # Get the results
    rows = cursor.fetchall()

    # Take the country name from each result row
    countries = [row[0] for row in rows]

    # Close the Snowflake connection
    cursor.close()
    connection.close()

    # Return the countries as JSON
    return {
        "countries": countries
    }

# Endpoint to get COVID data for a specific country
@app.get("/covid/{country}")
def get_covid_data(country: str):

    connection = get_snowflake_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            TO_CHAR(DATE, 'YYYY-MM-DD'),
            CASES,
            DEATHS,
            POPULATION,
            DENSITY_P_KM2,
            LIFE_EXPECTANCY,
            OUT_OF_POCKET_HEALTH_EXPENDITURE
        FROM COVID_PROJECT_DB.ANALYTICS.COVID_GOLD_TABLE
        WHERE UPPER(TRIM(COUNTRY_REGION)) = UPPER(TRIM(%s))
        ORDER BY DATE
        """,
        (country,),
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    data = []

    for row in rows:
        data.append(
            {
                "date": row[0],
                "cases": row[1],
                "deaths": row[2],
                "population": row[3],
                "density_p_km2": row[4],
                "life_expectancy": row[5],
                "health_expenditure": row[6],
            }
        )

    return {
        "country": country,
        "data": data,
    }

# Endpoint to get the list of vaccines
@app.get("/vaccines")
def get_vaccines():

    # Connect to Snowflake
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    # Get unique vaccine names
    cursor.execute(
        """
        SELECT DISTINCT VACCINE
        FROM COVID_PROJECT_DB.ANALYTICS.COUNTRY_VACCINES
        WHERE VACCINE IS NOT NULL
        ORDER BY VACCINE
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # Create a simple list
    vaccines = []

    for row in rows:
        vaccines.append(row[0])

    return {
        "vaccines": vaccines
    }

# Endpoint to get vaccines for a specific country
@app.get("/vaccines/{country}")
def get_country_vaccines(country: str):

    # Connect to Snowflake
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    # Get vaccines for the selected country
    cursor.execute(
        """
        SELECT DISTINCT VACCINE
        FROM COVID_PROJECT_DB.ANALYTICS.COUNTRY_VACCINES
        WHERE UPPER(COUNTRY_REGION) = UPPER(%s)
        ORDER BY VACCINE
        """,
        (country,),
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # Check whether Snowflake found the country
    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"Country '{country}' was not found",
        )


    # Create a list of vaccines
    vaccines = []

    for row in rows:
        vaccines.append(row[0])

    return {
        "country": country,
        "vaccines": vaccines,
    }



# Endpoint to get countries by vaccine
@app.get("/countries-by-vaccine")
def get_countries_by_vaccine(vaccine: str):

    connection = get_snowflake_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT DISTINCT COUNTRY_REGION
        FROM COVID_PROJECT_DB.ANALYTICS.COUNTRY_VACCINES
        WHERE UPPER(TRIM(VACCINE)) = UPPER(TRIM(%s))
        ORDER BY COUNTRY_REGION
        """,
        (vaccine,),
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    countries = []

    for row in rows:
        countries.append(row[0])

    return {
        "vaccine": vaccine,
        "countries": countries,
    }

# Endpoint to get vaccine summary
@app.get("/vaccine-summary")
def get_vaccine_summary():

    connection = get_snowflake_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            VACCINE,
            COUNT(DISTINCT COUNTRY_REGION) AS COUNTRY_COUNT
        FROM COVID_PROJECT_DB.ANALYTICS.COUNTRY_VACCINES
        WHERE VACCINE IS NOT NULL
        GROUP BY VACCINE
        ORDER BY COUNTRY_COUNT DESC
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    data = []

    for row in rows:
        data.append(
            {
                "vaccine": row[0],
                "country_count": row[1],
            }
        )

    return {
        "data": data
    }

# Endpoint to get comments from MongoDB
@app.get("/comments")
def get_comments():

    # Connect to MongoDB
    client = MongoClient(
        mongodb_uri,
        serverSelectionTimeoutMS=5000,
    )

    # Select the database and collection
    database = client["covid-project"]
    comments_collection = database["comments"]

    # Get all comments
    documents = comments_collection.find()

    comments = []

    for document in documents:

        created_at = document.get("created_at")

        comments.append(
            {
                "id": str(document["_id"]),
                "country": document.get("country"),
                "comment": document.get("comment"),
                "created_at": (
                    created_at.isoformat()
                    if created_at
                    else None
                ),
            }
        )

    client.close()

    return {
        "comments": comments
    }

#endpoint to add a comment to MongoDB
@app.post("/comments")
def add_comment(new_comment: Comment):

    # Connect to MongoDB
    client = MongoClient(
        mongodb_uri,
        serverSelectionTimeoutMS=5000,
    )

    # Select the database and collection
    database = client["covid_project"]
    comments_collection = database["comments"]

    # Create the MongoDB document
    document = {
        "country": new_comment.country,
        "comment": new_comment.comment,
        "created_at": datetime.now(timezone.utc),
    }

    # Save the document
    result = comments_collection.insert_one(document)

    client.close()

    return {
        "message": "Comment saved",
        "comment_id": str(result.inserted_id),
    }