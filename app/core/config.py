from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI MongoDB"
    PROJECT_VERSION: str = "0.1.0"

    # Base de datos
    MONGO_URI: str
    DATABASE_NAME: str

    # Autenticación JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int
    
    # Configuración de Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # Configuración del entorno
    ENVIRONMENT: str = "development"  # Puede ser "development" o "production"

    class Config:
        env_file = ".env"  # Cargar variables de entorno desde .env

settings = Settings()
