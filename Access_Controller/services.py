from fastapi import HTTPException
from pymongo import MongoClient
import hashlib

# MongoDB connection parameters
username = "username"
password = "pasword"
cluster_url = ".mongodb.net"
database_name = "student_account_database"

# Connect to MongoDB
client = mongouri
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
                raise HTTPException(status_code=401, detail="Account is locked Please Contact Admin.")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized user not available")
