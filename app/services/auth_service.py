from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.models.user import User
from app.core.config import settings  # Importamos configuración desde el .env
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Optional, Dict
from uuid import uuid4

# Usamos valores de .env en lugar de quemarlos en el código
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

refresh_tokens_db: Dict[str, str] = {}

async def get_user(email: str):
    return await User.find_one({"email": email})

async def create_user(email: str, password: str, full_name: Optional[str]):
    hashed_password = pwd_context.hash(password)
    user = User(email=email, hashed_password=hashed_password, full_name=full_name)
    await user.insert()
    return user

async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(email: str):
    refresh_token = str(uuid4())
    refresh_tokens_db[refresh_token] = email
    return refresh_token

async def refresh_access_token(refresh_token: str):
    email = refresh_tokens_db.get(refresh_token)
    if not email:
        raise HTTPException(status_code=401, detail="Refresh Token inválido o expirado")
    
    new_access_token = create_access_token(data={"sub": email})
    return {"access_token": new_access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        user = await get_user(email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
