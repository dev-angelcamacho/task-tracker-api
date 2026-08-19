from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

# Importamos nuestra BD y modelos
import models
from database import engine, get_db

# Crea las tablas en el archivo tasks.db si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- ESQUEMAS PYDANTIC (Validación de entrada/salida HTTP) ---
class PersonaCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False

class PersonaResponse(PersonaCreate):
    id: int

    class Config:
        from_attributes = True

# --- ENDPOINTS CON BASE DE DATOS ---

@app.get("/api/Personas", response_model=list[PersonaResponse])
def get_all_personas(db: Session = Depends(get_db)):
    # Consulta SQL equivalente a: SELECT * FROM personas;
    return db.query(models.PersonaModel).all()

@app.post("/api/Personas", response_model=PersonaResponse, status_code=201)
def create_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    # Crear instancia del modelo SQLAlchemy
    new_persona = models.PersonaModel(
        title=persona.title,
        description=persona.description,
        is_completed=persona.is_completed
    )
    db.add(new_persona)      # Agregar a la transacción
    db.commit()          # Guardar cambios en el archivo personas.db
    db.refresh(new_persona)   # Obtener el ID autogenerado
    return new_persona

@app.get("/api/Personas/{persona_id}", response_model=PersonaResponse)
def get_persona(persona_id: int, db: Session = Depends(get_db)):
    persona = db.query(models.PersonaModel).filter(models.PersonaModel.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@app.put("/api/Personas/{persona_id}", response_model=PersonaResponse)
def update_persona(persona_id: int, updated_persona: PersonaCreate, db: Session = Depends(get_db)):
    persona = db.query(models.PersonaModel).filter(models.PersonaModel.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
    # Actualizar campos
    persona.title = updated_persona.title
    persona.description = updated_persona.description
    persona.is_completed = updated_persona.is_completed
    
    db.commit()  # Guardar cambios
    db.refresh(persona)  # Refrescar instancia
    return persona

@app.delete("/api/Personas/{persona_id}", status_code=204)
def delete_persona(persona_id: int, db: Session = Depends(get_db)):
    persona = db.query(models.PersonaModel).filter(models.PersonaModel.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
    db.delete(persona)  # Eliminar de la transacción
    db.commit()         # Guardar cambios
    return None  # Retorna 204 No Content