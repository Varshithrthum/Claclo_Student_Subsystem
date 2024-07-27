from fastapi import APIRouter, HTTPException
from .services import create_profile, download_profile, print_profile, update_profile
from .models import Profile

profile_manager_router = APIRouter()

@profile_manager_router.post("/create_profile/")
async def create_profile_handler(profile: Profile):
    return await create_profile(profile)

@profile_manager_router.put("/update_profile/")
async def update_profile_handler(user_id: str, updated_data: Profile):
    return await update_profile(user_id, updated_data)

@profile_manager_router.get("/download_profile/")
async def download_profile_handler(user_id: str):
    return await download_profile(user_id)

@profile_manager_router.get("/Print_profile/")
async def print_profile_handler(user_id: str):
    return await print_profile(user_id)