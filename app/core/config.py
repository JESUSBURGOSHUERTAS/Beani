from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI MongoDB"
    PROJECT_VERSION: str = "0.1.0"

    # Base de datos
    MONGO_URI: str
    DATABASE_NAME: str

    # Configuración del entorno
    ENVIRONMENT: str = "development"  # Puede ser "development" o "production"

    class Config:
        env_file = ".env"  # Cargar variables de entorno desde .env

settings = Settings()
