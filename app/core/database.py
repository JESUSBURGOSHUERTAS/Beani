import importlib
import pkgutil
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
import app.models  # Asegura que se importan los modelos

# Conexión a MongoDB
client = AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.DATABASE_NAME]

async def init_db():
    print("🔗 Conectando a MongoDB e inicializando Beanie...")

    # Detectar y cargar modelos desde __all__ en app/models/
    models = []
    detected_models = []

    for model_name in getattr(app.models, "__all__", []):
        model = getattr(app.models, model_name, None)
        if model:
            models.append(model)
            detected_models.append(model.__name__)  # Obtener nombre de la clase
    
    await init_beanie(database, document_models=models)

    print(f"📂 Modelos detectados: {detected_models}")
    print("✅ Beanie inicializado correctamente")
