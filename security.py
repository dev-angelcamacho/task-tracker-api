# Crear Archivo de seguridad para la API
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt


# configuracion de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de token JWT
SECRET_KEY = "Super_secreta1234567890"  # Cambiar a una clave segura en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Duración del token en minutos

def hash_password(password: str) -> str:
    # Recortamos la contraseña a un máximo de 72 bytes por seguridad del algoritmo bcrypt
    pwd_bytes = password.encode('utf-8')[:72]
    return pwd_context.hash(pwd_bytes.decode('utf-8', errors='ignore'))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)