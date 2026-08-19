from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

import models
import schemas
import crud
import security
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Personas", description="API para gestionar personas", version="1.0.0")


# 👈 2. Configurar el Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permite todas las cabeceras (incluyendo Authorization para el JWT)
)    


# Integración con el sistema de Swagger Docs para el botón "Authorize"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
# security_scheme = HTTPBearer()


# --- ENDPOINTS DE AUTENTICACIÓN ---

@app.post("/api/auth/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El correo electrónico ya está registrado")

    return crud.create_user(db=db, user=user)

@app.post("/api/auth/login", response_model=schemas.Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm usa la propiedad 'username' para capturar el email ingresado
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Si las credenciales son válidas, generamos el JWT
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


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

# --- ENDPOINT PROTEGIDO DE PRUEBA ---

@app.get("/api/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.UserModel = Depends(get_current_user)):
    return current_user











## --- ENDPOINTS Logicos de Negocio. En este caso Personas ---

# ---- GET ----- Traer todas las personas
@app.get("/api/personas", response_model=list[schemas.PersonaResponse])
def get_all_personas(db: Session = Depends(get_db)):
    return crud.get_personas(db)

# ---- POST ----- Crear una nueva persona
@app.post("/api/personas", response_model=schemas.PersonaResponse)
def create_persona(persona: schemas.PersonaCreate, db: Session = Depends(get_db)):
    return crud.create_persona(db, persona)

# --- GET ----- Traer persona por ID
@app.get("/api/personas/{persona_id}", response_model=schemas.PersonaResponse)
def get_persona_by_id(persona_id: int, db: Session = Depends(get_db)):
    persona = crud.get_persona(db, persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

# --- PUT ----- Actualizar persona por ID
@app.put("/api/personas/{persona_id}", response_model=schemas.PersonaResponse)
def update_persona(persona_id: int, persona: schemas.PersonaCreate, db: Session = Depends(get_db)):
    db_persona = crud.get_persona(db, persona_id)
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return crud.update_persona(db, db_persona, persona)

# --- DELETE ----- Eliminar persona por ID
@app.delete("/api/personas/{persona_id}", response_model=schemas.PersonaResponse)
def delete_persona(persona_id: int, db: Session = Depends(get_db)):
    db_persona = crud.get_persona(db, persona_id)
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return crud.delete_persona(db, db_persona)