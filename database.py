import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Si existe DATABASE_URL (ej. en Docker o Render) usa PostgreSQL, de lo contrario cae en SQLite local
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# SQLite requiere un argumento extra que PostgreSQL no necesita
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Crear fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base para los modelos ORM
Base = declarative_base()

# Dependencia para obtener la sesión de BD en cada endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()