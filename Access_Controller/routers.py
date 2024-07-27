
from fastapi import APIRouter, HTTPException
from .services import authenticate_user

access_authentication_router = APIRouter()

@access_authentication_router.post("/authenticate_user/")
async def authenticate_user_handler(username: str, password: str):
    return await authenticate_user(username, password)