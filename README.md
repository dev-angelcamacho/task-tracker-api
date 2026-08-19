# Task Tracker API & Frontend

Un sistema full-stack desacoplado para la gestión y seguimiento de tareas diarias. El proyecto implementa una arquitectura cliente-servidor moderna con un backend enfocado en alto rendimiento y una interfaz de usuario reactiva de tipo SPA (Single Page Application).

---

## 🛠️ Tecnologías Utilizadas

### Backend
* **Python** (FastAPI) - Framework asíncrono de alto rendimiento para el desarrollo de la API REST.
* **SQLAlchemy** - ORM para el mapeo objeto-relacional y gestión de la base de datos.
* **Pydantic** - Validación estricta de datos y serialización de esquemas.
* **OAuth2 + JWT** (`python-jose`) - Autenticación y autorización basada en tokens.
* **Passlib / Bcrypt** - Hashing seguro de contraseñas.
* **Pytest** - Suite de pruebas unitarias e integración.

### Frontend
* **React** - Librería para la construcción de la interfaz de usuario basada en componentes.
* **Vite** - Bundler y entorno de desarrollo rápido para el frontend.
* **Bootstrap** - Framework CSS para diseño responsivo y componentes UI.
* **Axios / Fetch** - Cliente HTTP para el consumo de endpoints de la API REST.

---
# 🚀 Instalación y Configuración Local

### Prerrequisitos
* Python 3.10+
* Node.js 18+ y npm
* Git

---

## 1. Configuración del Backend

### 1.1 Navega a la carpeta del backend:
      cd backend

### 1.2 Crea y activa un entorno virtual:
   #### Linux / macOS
       python3 -m venv venv
       source venv/bin/activate
   #### Windows
       python -m venv venv
       .\venv\Scripts\activate
### 1.3 Instala las dependencias:
      pip install -r requirements.txt
   
### 1.4 Ejecuta el servidor de desarrollo:
      uvicorn app.main:app --reload

### 1.5 Accede a la documentación interactiva de la API:   
          Swagger UI: http://127.0.0.1:8000/docs
          ReDoc: http://127.0.0.1:8000/redoc

---
## 2. Configuración del Frontend

### 2.1 En una nueva terminal, navega a la carpeta del frontend:

      cd frontend
      
### 2.2 Instala las dependencias del proyecto:
      npm install
      
### 2.3 Inicia el servidor de desarrollo:
      npm run dev

### 2.4 Abre tu navegador e ingresa a: 
      http://localhost:5173 (o la URL indicada en la consola).

---
# 🧪 Pruebas Automatizadas
### Para ejecutar las pruebas del backend, asegúrate de tener el entorno virtual activo y ejecuta:
      cd backend
      pytest
---
# ✒️ Autor
Desarrollador Junior / Analista de Soportes Digitales / 

GitHub: @dev-angelcamacho


---
# 📐 Arquitectura del Sistema

El proyecto sigue un patrón de **Arquitectura Desacoplada (Decoupled Architecture)** con separación clara de responsabilidades:

```text
[ Base de Datos ] 
       ▲
       │ (SQL / SQLAlchemy ORM)
       ▼
[ Backend: FastAPI ] <─── (JSON / REST API over HTTP) ───> [ Frontend: React SPA ]
  • Routers / Endpoints                                     • UI Components
  • Pydantic Schemas                                        • State Management
  • Business Services                                       • Axios Services


task-tracker-api/
├── backend/                  # Código fuente del Servidor / API
│   ├── app/
│   │   ├── api/             # Endpoints y rutas de la API REST
│   │   ├── core/            # Configuraciones globales y seguridad (JWT, Hash)
│   │   ├── crud/            # Operaciones de base de datos / Lógica de negocio
│   │   ├── models/          # Modelos de SQLAlchemy (Entidades de BD)
│   │   └── schemas/         # Esquemas de Pydantic (Validación DTO)
│   ├── tests/               # Pruebas automatizadas con Pytest
│   └── requirements.txt     # Dependencias de Python
│
├── frontend/                 # Código fuente del Cliente / React SPA
│   ├── src/
│   │   ├── assets/          # Archivos estáticos e imágenes
│   │   ├── components/      # Componentes UI reutilizables
│   │   ├── pages/           # Vistas / Pantallas principales
│   │   └── services/        # Configuración de clientes HTTP (Axios)
│   ├── package.json         # Dependencias de Node.js
│   └── vite.config.js       # Configuración del bundler Vite
│
└── README.md                 # Documentación del proyecto
