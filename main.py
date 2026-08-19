from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


# --- 1. MODELO DE DATOS (Pydantic) ---
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_completed: bool = False

# --- 2. BASE DE DATOS EN MEMORIA ---
db: list[Task] = []

# --- 3. ENDPOINTS ---

# GET: Obtener todas las tareas
@app.get("/")
def Inicio():
    return {"message": "Hola, bienvenido a la API de tareas. Usa /api/tasks para interactuar con las tareas."}


@app.get("/api/v1/tasks")
def get_all_tasks():
    print("Se ha recibido una solicitud GET para obtener todas las tareas")
    return db


# POST: Crear una nueva tarea
@app.post("/api/v1/tasks", status_code=201)
def create_task(task: Task):
    print("Se ha recibido una solicitud POST para crear una nueva tarea:", task)

    if any(existing_task.id == task.id for existing_task in db):
        raise HTTPException(status_code=400, detail="La tarea con este ID ya existe")
    else:
        db.append(task)
    return task


# GET: Obtener una tarea por ID
@app.get("/api/v1/tasks/{task_id}")
def get_task(task_id: int):
    print("Se ha recibido una solicitud GET para obtener la tarea con ID:", task_id)
    for task in db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


# PUT: Actualizar una tarea por ID
@app.put("/api/v1/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    print("Se ha recibido una solicitud PUT para actualizar la tarea con ID:", task_id)
    for i, task in enumerate(db):
        if task.id == task_id:
            db[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


# DELETE: Eliminar una tarea por ID
@app.delete("/api/v1/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    print("Se ha recibido una solicitud DELETE para eliminar la tarea con ID:", task_id)
    for i, task in enumerate(db):
        if task.id == task_id:
            del db[i]
            return
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


# GET
@app.get("/api/v2/personas")
def get_personas():    
    return {"message": "Aquí se devolverían todas las personas."}

# POST
@app.post("/api/v2/personas", status_code=201)
def create_persona(persona: dict):
    return persona

# PUT
@app.put("/api/v2/personas/{persona_id}")
def update_persona(persona_id: int, updated_persona: dict):
    return {"message": f"Persona con ID {persona_id} actualizada."}

# DELETE
@app.delete("/api/v2/personas/{persona_id}", status_code=204)
def delete_persona(persona_id: int):
    return {"message": f"Persona con ID {persona_id} eliminada."}




# ===============================================================================
# ===============================================================================
# ===============================================================================
# ===============================================================================
# ===============================================================================
# ===============================================================================