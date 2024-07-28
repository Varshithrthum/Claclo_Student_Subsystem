# services.py

from pymongo import MongoClient
from urllib.parse import quote_plus
from typing import Optional
import os

# Load sensitive information from environment variables
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster_url = os.getenv("MONGO_CLUSTER_URL")
database_name = os.getenv("MONGO_DATABASE_NAME")

# Escape username and password
escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

# MongoDB connection string
mongo_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@{cluster_url}/{database_name}?retryWrites=true&w=majority&appName=Comp7033"

class MongoDBService:
    @classmethod
    def get_assessment_details(cls, user_id: str, assignment_id: str) -> Optional[dict]:
        try:
            # Connect to MongoDB
            client = MongoClient(mongo_uri)
            db = client[database_name]
            
            # Query the AssessmentDetails collection
            assessment_details_data = db.AssessmentDetails.find_one(
                {"user_id": user_id, "assignment_id": assignment_id},
                {"_id": 0, "user_id": 1, "assignment_id": 1, "assessment_details": 1}
            )
            
            # Close MongoDB connection
            client.close()
            
            return assessment_details_data
        except Exception as e:
            raise e

    @classmethod
    def submit_assessment(cls, user_id: str, assignment_id: str, submission_details: dict) -> bool:
        try:
            # Connect to MongoDB
            client = MongoClient(mongo_uri)
            db = client[database_name]
            
            # Insert submission details into the Submissions collection
            db.submissions.insert_one({
                "user_id": user_id,
                "assignment_id": assignment_id,
                "submission_details": submission_details
            })
            
            # Close MongoDB connection
            client.close()
            
            return True
        except Exception as e:
            raise e
