from app.models.task import Task, UpdateTask
from typing import List, Optional

# Crear una nueva tarea
async def create_task(task: Task) -> Task:
    return await task.insert()  # Inserta el documento en MongoDB

# Obtener todas las tareas
async def get_tasks() -> List[Task]:
    return await Task.find_all().to_list()

# Obtener una tarea por ID
async def get_task(task_id: str) -> Optional[Task]:
    return await Task.get(task_id)

# Actualizar una tarea
async def update_task(task_id: str, task_data: UpdateTask) -> Optional[Task]:
    task = await Task.get(task_id)
    if task:
        update_data = task_data.model_dump(exclude_unset=True)
        await task.update({"$set": update_data})
        return task
    return None

# Eliminar una tarea
async def delete_task(task_id: str) -> bool:
    task = await Task.get(task_id)
    if task:
        await task.delete()
        return True
    return False
