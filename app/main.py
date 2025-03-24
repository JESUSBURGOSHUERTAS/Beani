from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Configurar CORS para permitir solicitudes desde https://localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Origen permitido
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Mensaje según el entorno
if settings.ENVIRONMENT == "development":
    print("🔧 Ejecutando en modo DESARROLLO")
else:
    print("🚀 Ejecutando en modo PRODUCCIÓN")

@app.get("/")
def welcome():
    return {"message": "Welcome to the FastAPI!"}

# Registrar rutas
app.include_router(task.router, prefix="/api/tasks", tags=["tasks"])

