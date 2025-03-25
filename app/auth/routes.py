from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from app.auth.utils import create_access_token, create_refresh_token, verify_token
from app.core.config import settings

router = APIRouter()

# Simulación de usuarios (luego lo reemplazaremos con MongoDB)
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "123456",  # ¡No uses esto en producción!
    }
}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    # Crear tokens
    access_token = create_access_token({"sub": user["username"]})
    refresh_token = create_refresh_token({"sub": user["username"]})

    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = verify_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Refresh token inválido o expirado")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Generar nuevo access token
    new_access_token = create_access_token({"sub": username})
    return {"access_token": new_access_token}
