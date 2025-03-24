from fastapi import FastAPI
from app.core.database import init_db
from contextlib import asynccontextmanager

from app.core.config import settings

from app.api.v1.routes import task
# from app.api.v1.routes.company import company

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Inicializar Beanie
    yield  # Continuar con la ejecución de la app

app = FastAPI(lifespan=lifespan)

# Mensaje según el entorno
if settings.ENVIRONMENT == "development":
    print("🔧 Ejecutando en modo DESARROLLO")
else:
    print("🚀 Ejecutando en modo PRODUCCIÓN")

@app.get("/")
def welcome():
    return {"message": "Welcome to the FastAPI!"}

# Registrar rutas
app.include_router(task.router, prefix="/tasks", tags=["tasks"])

