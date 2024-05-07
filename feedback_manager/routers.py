from fastapi import APIRouter, HTTPException
from .services import MongoDBService
from .models import FeedbackDetails

feedback_router = APIRouter()

@feedback_router.get("/feedback/")
async def get_feedback(user_id: str, assignment_id: str):
    try:
        feedback_data = MongoDBService.get_feedback(user_id, assignment_id)
        if feedback_data:
            return feedback_data
        else:
            raise HTTPException(status_code=404, detail="Feedback not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))