# models.py

from pydantic import BaseModel

class AssessmentDetails(BaseModel):
    user_id: str
    assignment_id: str
    assessment_details: str

class SubmissionDetails(BaseModel):
    user_id: str
    assignment_id: str
    submission_details: str
