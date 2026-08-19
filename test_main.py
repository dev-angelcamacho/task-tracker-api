import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine
import models

client = TestClient(app)

# Crear todas las tablas en la base de datos antes de que se ejecuten los tests
Base.metadata.create_all(bind=engine)

def test_read_main():
    response = client.get("/docs")
    assert response.status_code == 200

def test_register_user_invalid_data():
    response = client.post("/api/auth/register", json={"email": "invalid"})
    assert response.status_code == 422

def test_unauthorized_access_personas():
    response = client.get("/api/personas")
    assert response.status_code == 401

def test_full_auth_and_persona_flow():
    # 1. Registro de usuario
    email = "testuser_pytest@example.com"
    password = "testpassword123"
    
    reg_response = client.post(
        "/api/auth/register",
        json={"email": email, "password": password}
    )
    assert reg_response.status_code in [201, 400]  # 201 si es nuevo, 400 si ya fue creado

    # 2. Autenticación y obtención del token Bearer
    login_response = client.post(
        "/api/auth/login",
        data={"username": email, "password": password}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Creación de Persona usando el token
    persona_data = {
        "name": "Prueba",
        "lastname": "Integration",
        "phone": "3000000000",
        "is_actived": True
    }
    create_response = client.post("/api/personas", json=persona_data, headers=headers)
    assert create_response.status_code == 201
    assert create_response.json()["name"] == "Prueba"

    # 4. Lectura paginada de Personas con autenticación
    get_response = client.get("/api/personas?skip=0&limit=5", headers=headers)
    assert get_response.status_code == 200
    assert isinstance(get_response.json(), list)