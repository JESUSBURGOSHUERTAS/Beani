from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(Document):
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    google_id: Optional[str] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        collection = "users"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserResponse(BaseModel):
    email: EmailStr
    full_name: Optional[str]
