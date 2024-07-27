from pydantic import BaseModel
from pymongo import MongoClient
from urllib.parse import quote_plus
from fastapi import APIRouter, FastAPI, HTTPException

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

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]

# Define MongoDB collections
students_collection = db["students"]
assessments_collection = db["AssessmentDetails"]
feedback_collection = db["feedback"] 
submissions_collection = db["submissions"]

# Models
class AssessmentDetails(BaseModel):
    user_id: str
    assignment_id: str
    assessment_details: str

class SubmissionDetails(BaseModel):
    user_id: str
    assignment_id: str
    submission_details: str

class FeedbackDetails(BaseModel):
    user_id: str
    assignment_id: str
    feedback: str
    grade: str

# Services
class MongoDBService:
    @classmethod
    def get_submission_details(cls, user_id: str, assignment_id: str):
        try:
            # Query the Submissions collection
            submission_details_data = db.submissions.find_one( 
                {"user_id": user_id, "assignment_id": assignment_id},
                {"_id": 0, "user_id": 1, "assignment_id": 1, "submission_details": 1}
            )
            return submission_details_data
        except Exception as e:
            raise e

    @classmethod
    def provide_feedback_and_grade(cls, user_id: str, assignment_id: str, feedback: str, grade: str):
        try:
            # Save feedback details in the Feedback collection
            feedback_data = {
                "user_id": user_id,
                "assignment_id": assignment_id,
                "feedback": feedback,
                "grade": grade
            }
            feedback_collection.insert_one(feedback_data)

            return True
        except Exception as e:
            # Log the error
            print("Error occurred while saving feedback:", e)
            raise e

# Test insertion directly into the feedback collection
try:
    test_feedback = {
        "user_id": "test_user_id",
        "assignment_id": "test_assignment_id",
        "feedback": "Test feedback",
        "grade": "A"
    }
    feedback_collection.insert_one(test_feedback)
    print("Test feedback inserted successfully.")
except Exception as e:
    print("Error occurred while inserting test feedback:", e)

# Routers
teacher_router = APIRouter()

@teacher_router.get("/submission_details/")
async def get_submission_details(user_id: str, assignment_id: str):
    try:
        submission_details_data = MongoDBService.get_submission_details(user_id, assignment_id)
        if submission_details_data:
            return submission_details_data
        else:
            raise HTTPException(status_code=404, detail="Submission details not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@teacher_router.post("/provide_feedback_and_grade/")
async def provide_feedback_and_grade(user_id: str, assignment_id: str, feedback: str, grade: str):
    try:
        success = MongoDBService.provide_feedback_and_grade(user_id, assignment_id, feedback, grade)
        if success:
            return {"message": "Feedback and grade provided successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to provide feedback and grade")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to post an assessment to all students
def post_assessment_to_all_students(assignment_id: str, assessment_details: str):
    # Get all students from the students collection
    all_students = students_collection.find({})
    
    # Iterate over all students
    for student in all_students:
        # Save the assessment for each student in the assessments collection
        assessment_data = {
            "user_id": student["user_id"],  
            "assignment_id": assignment_id,
            "assessment_details": assessment_details
        }
        assessments_collection.insert_one(assessment_data)
    
    return {"message": "Assessment posted to all students successfully"}

# Endpoint to post an assessment to all students
@teacher_router.post("/post_assessment_to_all_students")
async def post_assessment_route(assignment_id: str, assessment_details: str):
    return post_assessment_to_all_students(assignment_id, assessment_details)

# Create FastAPI app
app = FastAPI()

# Include router
app.include_router(teacher_router)
