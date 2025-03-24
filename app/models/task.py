from beanie import Document
from pydantic import BaseModel
from typing import Optional

# Modelo principal con Beanie
class Task(Document):
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Settings:
        collection = "tasks"  # Nombre de la colección en MongoDB

# Modelo para actualización de tareas
class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
