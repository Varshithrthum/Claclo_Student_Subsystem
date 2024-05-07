
from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    password: str

class AuthenticationResponse(BaseModel):
    status: str

