from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.jwt_handler import create_access_token
from app.auth.dependencies import get_current_user

router = APIRouter()

# Ruta para iniciar sesión y generar un token
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Simulación de usuario (reemplazar con BD más adelante)
    fake_user_db = {
        "admin": {"username": "admin", "password": "123456"}
    }

    user = fake_user_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

# Ruta protegida para verificar el token
@router.get("/perfil")
async def perfil(usuario: dict = Depends(get_current_user)):
    return {"message": "Bienvenido", "usuario": usuario}
