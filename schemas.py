from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


# --- ESQUEMAS PYDANTIC (Validación de entrada/salida HTTP) ---
class PersonaCreate(BaseModel):
    name: str
    lastname: str
    phone: int
    is_actived: bool = False

# Hacemos que herede de PersonaCreate
class PersonaResponse(PersonaCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


# --- Esquema para token de respuesta ---
class Token(BaseModel):
    access_token: str
    token_type: str