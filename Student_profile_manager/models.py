from pydantic import BaseModel

class Profile(BaseModel):
    user_id: str
    password: str  
    first_name: str
    last_name: str
    email: str
    street: str
    city: str
    state: str
    country: str
    postcode: str
    
    
