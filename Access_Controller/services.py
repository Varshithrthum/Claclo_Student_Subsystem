from fastapi import HTTPException
from pymongo import MongoClient
import hashlib
import os

# Load sensitive information from environment variables
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster_url = os.getenv("MONGO_CLUSTER_URL")
database_name = os.getenv("MONGO_DATABASE_NAME")

# Construct MongoDB URI
mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/{database_name}?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]

# Define MongoDB collections
users_collection = db["Security"]

async def authenticate_user(user_id: str, password: str) -> str:
    # Hash the provided password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Retrieve the user from the database
    user = users_collection.find_one({"user_id": user_id})
    if user:
        # Compare the hashed password with the one stored in the database
        if user.get("password") == hashed_password:
            return "Authentication Successful"
        else:
            # Check if the user has any remaining attempts
            remaining_attempts = user.get("remaining_attempts", 3)
            if remaining_attempts > 1:
                # Decrement the remaining attempts
                users_collection.update_one({"user_id": user_id}, {"$set": {"remaining_attempts": remaining_attempts - 1}})
                raise HTTPException(status_code=401, detail=f"Incorrect password. {remaining_attempts - 1} tries remaining.")
            else:
                # Lock the user account
                users_collection.update_one({"user_id": user_id}, {"$set": {"account_status": "locked"}})
                raise HTTPException(status_code=401, detail="Account is locked. Please contact Admin.")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized user not available")
