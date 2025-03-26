from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.services.auth_service import (
    create_user, authenticate_user, create_access_token, create_refresh_token, refresh_access_token, get_current_user
)
from app.services.google_auth_service import google_auth
from app.models.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    existing_user = await authenticate_user(user_data.email, user_data.password)
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    user = await create_user(user_data.email, user_data.password, user_data.full_name)
    return UserResponse(email=user.email, full_name=user.full_name)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=60))
    refresh_token = create_refresh_token(user.email)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh")
async def refresh(token: str):
    return await refresh_access_token(token)

@router.get("/me", response_model=UserResponse)
async def get_me(user: UserResponse = Depends(get_current_user)):
    return user

@router.get("/login/google")
async def login_google(code: str):
    user = await google_auth(code)
    if not user:
        raise HTTPException(status_code=400, detail="Error en autenticación con Google")
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=60))
    refresh_token = create_refresh_token(user.email)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
