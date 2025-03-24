import importlib
import pkgutil
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
import app.models  # Importamos el paquete de modelos

# Conexión a MongoDB
client = AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.DATABASE_NAME]

# Función para cargar automáticamente todos los modelos en la carpeta models/
def load_models():
    models = []
    package = app.models  # Carpeta donde están los modelos

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"app.models.{module_name}")
        for attr in dir(module):
            obj = getattr(module, attr)
            if hasattr(obj, "__beanie__"):  # Filtra solo los modelos de Beanie
                models.append(obj)

    return models

# Inicialización de Beanie con carga automática de modelos
async def init_db():
    print("🔗 Conectando a MongoDB e inicializando Beanie...")
    models = load_models()
    await init_beanie(database, document_models=models)
    print("✅ Beanie inicializado correctamente")