from pydantic import BaseModel

class FeedbackDetails(BaseModel):
    user_id: str
    assignment_id: str
    feedback: str
    grade: str
