from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI MongoDB"
    PROJECT_VERSION: str = "0.1.0"

    # Base de datos
    MONGO_URI: str
    DATABASE_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Expira en 30 minutos
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # Expira en 7 días

    # Configuración del entorno
    ENVIRONMENT: str = "development"  # Puede ser "development" o "production"

    class Config:
        env_file = ".env"  # Cargar variables de entorno desde .env

settings = Settings()
