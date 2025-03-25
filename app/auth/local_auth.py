from fastapi import APIRouter, HTTPException, Depends
from app.models.user_model import User, UserCreate, UserResponse, AuthProvider
from app.auth.jwt_handler import create_access_token
from passlib.context import CryptContext
from beanie import PydanticObjectId

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    hashed_password = hash_password(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_password, auth_provider=AuthProvider.local)
    await new_user.insert()
    return new_user

@router.post("/login")
async def login_user(user_data: UserCreate):
    user = await User.find_one(User.email == user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}
