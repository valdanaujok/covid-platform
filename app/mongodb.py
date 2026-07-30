import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient


# Load settings from the .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Get the MongoDB connection address
mongodb_uri = os.getenv("MONGODB_URI")

try:
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)

    # Check the connection
    client.admin.command("ping")
    print("Connected to MongoDB!")

    # Select a database
    database = client["covid-project"]

    # Select a collection
    comments = database["comments"]

    # Create a comment
    comment = {
        "country": "Lithuania",
        "comment": "This is my first test comment.",
        "created_at": datetime.now(timezone.utc),
    }

    # Save the comment
    result = comments.insert_one(comment)

    print("Comment saved!")
    print(f"Comment ID: {result.inserted_id}")

except Exception as error:
    print("Something went wrong:")
    print(error)

finally:
    if "client" in locals():
        client.close()