from fastapi import FastAPI
from Student_profile_manager.routers import profile_manager_router
from Assessment_Manager.routers import assessment_router
from Access_Controller.routers import access_authentication_router
from feedback_manager.routers import feedback_router

from Dummy_Apis.Teacher import teacher_router
app = FastAPI()

# Include the AUTH manager router with appropriate tags
app.include_router(
    access_authentication_router,
    prefix="/Authentication",
    tags=["Access Controller"]
)


# Include the profile manager router with appropriate tags
app.include_router(
    profile_manager_router,
    prefix="/profile",
    tags=["Student_Profile_Manager"]
)

# Include the assessment manager router with appropriate tags
app.include_router(
    assessment_router,
    prefix="/assessment",
    tags=["Assessment_Manager"]
)
# Include the feedback manager router with appropriate tags
app.include_router(
    feedback_router,
    prefix="/feedback",
    tags=["Feedback_manager"]
)
# Include the dummy teacher api router with appropriate tags
app.include_router(
    teacher_router,
    prefix="/teacher",
    tags=["teacher"]
)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
