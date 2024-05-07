# router.py

from fastapi import APIRouter, HTTPException
from .services import MongoDBService
from .models import AssessmentDetails , SubmissionDetails

assessment_router = APIRouter()

@assessment_router.get("/assessment_details/")
async def get_assessment_details(user_id: str, assignment_id: str):
    try:
        assessment_details = MongoDBService.get_assessment_details(user_id, assignment_id)
        if assessment_details:
            return assessment_details
        else:
            raise HTTPException(status_code=404, detail="Assessment details not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@assessment_router.post("/submit_assessment/")
async def submit_assessment(user_id: str, assignment_id: str, submission_details: SubmissionDetails):
    try:
        success = MongoDBService.submit_assessment(user_id, assignment_id, submission_details.dict())
        if success:
            return {"message": "Assessment submitted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to submit assessment")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))