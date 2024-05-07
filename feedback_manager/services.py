from pymongo import MongoClient
from urllib.parse import quote_plus

# MongoDB connection parameters
username = "19275759"
password = "Brookes"
cluster_url = "comp7033.oynlmsu.mongodb.net"
database_name = "student_account_database"

# Escape username and password
escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

# MongoDB connection string
mongo_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@{cluster_url}/{database_name}?retryWrites=true&w=majority"

class MongoDBService:
    @classmethod
    def get_feedback(cls, user_id: str, assignment_id: str):
        try:
            # Connect to MongoDB
            client = MongoClient(mongo_uri)
            db = client[database_name]

            # Query the feedback collection
            feedback_collection = db["feedback"]
            feedback_data = feedback_collection.find_one(
                {"user_id": user_id, "assignment_id": assignment_id},
                {"_id": 0}
            )
            return feedback_data
        except Exception as e:
            raise e
