from sqlalchemy.orm import Session
import models
import schemas
import security


# Listar todos
def get_personas(db: Session):
    return db.query(models.PersonaModel).all()

# Obtener por ID
def get_persona_by_id(db: Session, persona_id: int):
    return db.query(models.PersonaModel).filter(models.PersonaModel.id == persona_id).first()

# Crear
def create_persona(db: Session, persona: schemas.PersonaCreate):
    new_persona = models.PersonaModel(
        name=persona.name,
        lastname=persona.lastname,
        phone=persona.phone,
        is_actived=persona.is_actived
    )
    db.add(new_persona)
    db.commit()
    db.refresh(new_persona)
    return new_persona

# Actualizar
def update_persona(db: Session, persona_db: models.PersonaModel, persona_data: schemas.PersonaCreate):
    persona_db.name = persona_data.name
    persona_db.lastname = persona_data.lastname
    persona_db.phone = persona_data.phone
    persona_db.is_actived = persona_data.is_actived
    
    db.commit()
    db.refresh(persona_db)
    return persona_db

# Eliminar
def delete_persona(db: Session, persona_db: models.PersonaModel):
    db.delete(persona_db)
    db.commit()
    return True




# --- LÓGICA DE  Seguridad USUARIOS ---

def get_user_by_email(db: Session, email: str):
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # Encriptamos la contraseña antes de guardarla en la BD
    hashed_password = security.hash_password(user.password)

    db_user = models.UserModel(
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user