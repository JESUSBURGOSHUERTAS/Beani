from fastapi import APIRouter, HTTPException
from app.services.task_service import (
    create_task, get_tasks, get_task, update_task, delete_task
)
from app.models.task import Task, UpdateTask
from typing import List

router = APIRouter()

# Crear una tarea
@router.post("/", response_model=Task)
async def create(task: Task):
    return await create_task(task)

# Obtener todas las tareas
@router.get("/", response_model=List[Task])
async def read_all():
    return await get_tasks()

# Obtener una tarea por ID
@router.get("/{task_id}", response_model=Task)
async def read(task_id: str):
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

# Actualizar una tarea
@router.put("/{task_id}", response_model=Task)
async def update(task_id: str, task_data: UpdateTask):
    updated_task = await update_task(task_id, task_data)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return updated_task

# Eliminar una tarea
@router.delete("/{task_id}", response_model=dict)
async def delete(task_id: str):
    if await delete_task(task_id):
        return {"message": "Tarea eliminada"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
