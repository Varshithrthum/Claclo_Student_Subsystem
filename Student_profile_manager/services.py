from pymongo import MongoClient
from urllib.parse import quote_plus
from fastapi import HTTPException
from Student_profile_manager.models import Profile
import hashlib

# MongoDB connection parameters
username = "19275759"
password = "Brookes"
cluster_url = "comp7033.oynlmsu.mongodb.net"
database_name = "student_account_database"

# Escape username and password
escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

# MongoDB connection string
mongo_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@{cluster_url}/{database_name}?retryWrites=true&w=majority&appName=Comp7033"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]

# Define MongoDB collections
students_collection = db["students"]
address_collection = db["Address"]
security_collection = db["Security"]

async def create_profile(profile: Profile):
    try:
        # Hash the password using hashlib
        hashed_password = hashlib.sha256(profile.password.encode()).hexdigest()

        # Insert profile data into MongoDB
        # Insert profile data into 'students' collection
        result = students_collection.insert_one({
            "user_id": profile.user_id,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "email": profile.email
        })

        # Insert address data into 'Address' collection
        address_result = address_collection.insert_one({
            "user_id": profile.user_id,
            "street": profile.street,
            "city": profile.city,
            "state": profile.state,
            "country": profile.country,
            "postcode": profile.postcode
        })

        # Insert security data into 'Security' collection
        security_result = security_collection.insert_one({
            "user_id": profile.user_id,
            "password": hashed_password
        })

        # Check if all insertions were successful
        if result.inserted_id and address_result.inserted_id and security_result.inserted_id:
            return {"message": "Profile created successfully", "profile_id": str(result.inserted_id)}
        else:
            # If any insertion failed, raise an exception
            raise HTTPException(status_code=500, detail="Failed to create profile")

    except Exception as e:
        # Log the error and raise an HTTPException
        print("Error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def download_profile(user_id: str):
    profile_data = students_collection.find_one({"user_id": user_id})
    if profile_data is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile_data.pop('_id', None)
    return profile_data

async def print_profile(user_id: str):
    profile_data = students_collection.find_one({"user_id": user_id})
    if profile_data is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile_data.pop('_id', None)
    return profile_data

async def update_profile(user_id: str, updated_data: Profile):
    try:
        print("Received user_id:", user_id)  
        print("Updated data:", updated_data.dict())  # Convert Pydantic model to dictionary for logging
        
        # Retrieve profile data from MongoDB
        profile_data = students_collection.find_one({"user_id": user_id})
        if profile_data is None:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Populate update fields with provided data, excluding fields that are None
        update_fields = {key: value for key, value in updated_data.dict().items() if value is not None}
        
        result = students_collection.update_one({"user_id": user_id}, {"$set": update_fields})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return {"message": "Profile updated successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print("Error occurred:", e)  # Log the error
        raise HTTPException(status_code=500, detail="Internal Server Error")
