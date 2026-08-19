# Task Tracker API & Frontend

Un sistema full-stack desacoplado para la gestión y seguimiento de tareas diarias. El proyecto implementa una arquitectura cliente-servidor moderna con un backend enfocado en alto rendimiento y una interfaz de usuario reactiva de tipo SPA (Single Page Application), orquestado completamente mediante contenedores con Docker Compose.

---

## 🛠️ Tecnologías Utilizadas

### Backend
* Python 3.10 (FastAPI) - Framework asíncrono de alto rendimiento para el desarrollo de la API REST.
* SQLAlchemy - ORM para el mapeo objeto-relacional y gestión de entidades de base de datos.
* Pydantic - Validación estricta de datos, serialización y esquemas DTO.
* OAuth2 + JWT (python-jose) - Autenticación y autorización basada en tokens Bearer.
* Passlib / Bcrypt - Hashing seguro de contraseñas.
* Pytest - Suite de pruebas unitarias e integración.

### Frontend
* React 18 - Librería para la construcción de la interfaz de usuario basada en componentes.
* Vite - Bundler de última generación y entorno de desarrollo rápido.
* Node.js 20 - Entorno de ejecución optimizado.
* Bootstrap - Framework CSS para diseño responsivo y componentes UI.
* Fetch API - Cliente HTTP adaptado para el consumo de endpoints en formato JSON y URL-encoded.

### Base de Datos & Infraestructura
* PostgreSQL 15 - Motor de base de datos relacional en contenedor independiente con chequeos de salud (healthcheck).
* Docker & Docker Compose - Containerización y orquestación unificada de servicios.

---

## 🐳 Despliegue Rápido con Docker Compose (Recomendado)

Todo el ecosistema (Base de Datos, Backend y Frontend) se puede ejecutar de forma orquestada con un solo comando.

### Prerrequisitos
* Docker Desktop instalado y en ejecución.
* Git.

### Pasos para iniciar:

1. Clonar el repositorio:
   git clone https://github.com/dev-angelcamacho/task-tracker-api.git
   cd task-tracker-api

2. Levantar el entorno completo:
   docker compose up --build

3. Servicios disponibles:
   * Frontend (React SPA): http://localhost:5173
   * Backend API (Swagger Docs): http://localhost:8080/docs
   * Base de Datos (PostgreSQL): localhost:5432 (User: postgres | DB: personas_db)

---

## 🚀 Instalación y Configuración Local (Sin Docker)

Si prefieres ejecutar los servicios directamente en tu máquina local:

### 1. Configuración del Backend

1.1 Crea y activa un entorno virtual:
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate

1.2 Instala las dependencias:
pip install -r requirements.txt

1.3 Ejecuta el servidor de desarrollo:
uvicorn main:app --reload --port 8000

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

---

### 2. Configuración del Frontend

2.1 Navega a la carpeta del frontend e instala dependencias:
cd frontend
npm install

2.2 Inicia el servidor de desarrollo:
npm run dev

2.3 Abre tu navegador en: http://localhost:5173

---

## 📐 Arquitectura del Sistema y Contenedores

El proyecto sigue una Arquitectura Desacoplada, orquestando tres contenedores vinculados dentro de la red privada de Docker:

[ Contenedor: postgres_db ]
       ▲  (Puerto Interno: 5432)
       │  (SQLAlchemy / PostgreSQL)
       ▼
[ Contenedor: fastapi_backend ] <─── (JSON / OAuth2 over HTTP) ───> [ Contenedor: react_frontend ]
  • Port: 8080:8000                                                    • Port: 5173:5173
  • Healthcheck de DB                                                  • Vite + Node 20
  • Middleware CORS                                                    • React SPA + Bootstrap

### Estructura del Proyecto



      task-tracker-api/
      │
      ├── Dockerfile                  # Construcción de la imagen Docker para FastAPI
      ├── docker-compose.yml          # Orquestador (PostgreSQL + Backend + Frontend)
      ├── main.py                     # Punto de entrada de la API REST (FastAPI)
      ├── crud.py                     # Operaciones de lectura y escritura en la BD
      ├── models.py                   # Modelos relacionales de SQLAlchemy
      ├── schemas.py                  # Esquemas Pydantic para validación DTO
      ├── security.py                 # Lógica de Hashing (Bcrypt) y generación JWT
      ├── database.py                 # Conexión al motor de PostgreSQL
      ├── requirements.txt            # Dependencias de Python
      │
      ├── frontend/                   # Código fuente del Cliente React
      │   ├── Dockerfile              # Construcción de la imagen Docker para React (Node 20)
      │   ├── src/
      │   │   ├── components/         # Componentes modulares (Login, Vistas, Forms)
      │   │   ├── services/           # Cliente HTTP para consumo de API REST
      │   │   └── App.jsx             # Componente raíz
      │   ├── package.json            # Dependencias de Node.js
      │   └── vite.config.js          # Configuración del bundler Vite
      │
      └── README.md                   # Documentación técnica del proyecto

---

## 🧪 Pruebas Automatizadas

Para ejecutar la suite de pruebas unitarias en el backend:
pytest

---

## ✒️ Autor

Ángel Camacho
Desarrollador Junior / Analista de Soportes Digitales
GitHub: @dev-angelcamacho
