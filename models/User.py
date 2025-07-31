# Pydantic models
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class TeamCreateRequest(BaseModel):
    user_id: str