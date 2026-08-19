from fastapi.testclient import TestClient
from main import app

# Creamos un cliente HTTP simulado con nuestra app
client = TestClient(app)

def test_acceso_denegado_sin_token():
    """Prueba que la ruta /api/users/me rechace peticiones sin JWT."""
    response = client.get("/api/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_flujo_completo_autenticacion():
    """Prueba el flujo: Registro -> Login -> Obtener Token -> Consultar Perfil Protegido."""
    
    test_email = "pruebabot@example.com"
    test_password = "password123"

    # 1. Probar Registro
    response_register = client.post(
        "/api/auth/register",
        json={"email": test_email, "password": test_password}
    )
    assert response_register.status_code == 201
    assert response_register.json()["email"] == test_email

    # 2. Probar Login y generación del Token JWT
    response_login = client.post(
        "/api/auth/login",
        data={"username": test_email, "password": test_password}
    )
    assert response_login.status_code == 200
    data = response_login.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    token = data["access_token"]

    # 3. Acceder a la ruta protegida enviando el Token en los Headers
    headers = {"Authorization": f"Bearer {token}"}
    response_me = client.get("/api/users/me", headers=headers)
    
    assert response_me.status_code == 200
    assert response_me.json()["email"] == test_email