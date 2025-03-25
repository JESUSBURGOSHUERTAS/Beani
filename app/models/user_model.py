from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class AuthProvider(str, Enum):
    local = "local"
    google = "google"

class User(Document):
    email: EmailStr
    hashed_password: Optional[str] = None  # Solo si es usuario local
    auth_provider: AuthProvider  # "local" o "google"

    class Settings:
        name = "users"  # Nombre de la colección en MongoDB

    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@ejemplo.com",
                "hashed_password": "hashedpassword123",
                "auth_provider": "local"
            }
        }

class UserCreate(BaseModel):
    email: EmailStr
    password: Optional[str]  # Se enviará solo en usuarios locales

class UserResponse(BaseModel):
    email: EmailStr
    auth_provider: AuthProvider
