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

## 📐 Arquitectura del Sistema

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
