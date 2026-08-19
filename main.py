import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from jose import JWTError, jwt

import models
import schemas
import crud
import security
from database import engine, get_db


def wait_for_db():
    """Valida la disponibilidad del engine importado antes de crear tablas."""
    retries = 10
    while retries > 0:
        try:
            with engine.connect() as conn:
                print("¡Conexión exitosa a la base de datos!")
                return
        except OperationalError:
            retries -= 1
            print(f"Base de datos no disponible aún, reintentando en 3 segundos... ({retries} intentos restantes)")
            time.sleep(3)
    raise Exception("No se pudo conectar a la base de datos.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento de inicio: Esperar a la DB y crear tablas de modelos
    wait_for_db()
    models.Base.metadata.create_all(bind=engine)
    yield
    # Evento de apagado (si se requiere cleanup futuro)


app = FastAPI(
    title="API de Gestión de Personas", 
    description="Sistema de registro y administración de personas con autenticación JWT", 
    version="1.0.0",
    lifespan=lifespan
)

# Configurar el Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Integración con el sistema de Swagger Docs para el botón "Authorize"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# --- DEPENDENCIA DE PROTECCIÓN DE RUTAS ---

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token de acceso",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user


# --- RUTAS DE AUTENTICACIÓN (USUARIOS) ---

@app.post("/api/auth/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El correo electrónico ya está registrado"
        )
    return crud.create_user(db=db, user=user)

@app.post("/api/auth/login", response_model=schemas.Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.UserModel = Depends(get_current_user)):
    return current_user


# --- ENDPOINTS PROTEGIDOS DE PERSONAS ---

@app.get("/api/personas", response_model=list[schemas.PersonaResponse])
def get_all_personas(
    db: Session = Depends(get_db), 
    current_user: models.UserModel = Depends(get_current_user)
):
    return crud.get_personas(db)

@app.post("/api/personas", response_model=schemas.PersonaResponse, status_code=status.HTTP_201_CREATED)
def create_persona(
    persona: schemas.PersonaCreate, 
    db: Session = Depends(get_db), 
    current_user: models.UserModel = Depends(get_current_user)
):
    return crud.create_persona(db, persona)

@app.get("/api/personas/{persona_id}", response_model=schemas.PersonaResponse)
def get_persona_by_id(
    persona_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.UserModel = Depends(get_current_user)
):
    persona = crud.get_persona_by_id(db, persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@app.put("/api/personas/{persona_id}", response_model=schemas.PersonaResponse)
def update_persona(
    persona_id: int, 
    persona: schemas.PersonaCreate, 
    db: Session = Depends(get_db), 
    current_user: models.UserModel = Depends(get_current_user)
):
    db_persona = crud.get_persona_by_id(db, persona_id)
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return crud.update_persona(db, db_persona, persona)

@app.delete("/api/personas/{persona_id}")
def delete_persona(
    persona_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.UserModel = Depends(get_current_user)
):
    db_persona = crud.get_persona_by_id(db, persona_id)
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    crud.delete_persona(db, db_persona)
    return {"message": "Persona eliminada correctamente"}