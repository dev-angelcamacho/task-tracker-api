const API_URL = 'http://127.0.0.1:8090/api';

// --- AUTENTICACIÓN ---


// 1. CONSUMO A LA API BackEnd FastAPI con JWT
export async function login(email, password) {
  // OAuth2PasswordRequestForm requiere x-www-form-urlencoded
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Error al iniciar sesión');
  }

  return await response.json(); // Retorna { access_token, token_type }
}


// 2.  Consumo a la API BackEnd FastAPI con JWT para registrar un nuevo usuario
export async function register(email, password) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Error al registrar usuario');
  }

  return await response.json();
}




// --- GESTIÓN DE PERSONAS LOGICA DE NEGOCIO DE LA API BACKEND ---

export async function getPersonas(token) {
  const response = await fetch(`${API_URL}/personas`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('Error al obtener la lista de personas');
  }

  return await response.json();
}

export async function createPersona(personaData, token) {
  const response = await fetch(`${API_URL}/personas`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(personaData),
  });

  if (!response.ok) {
    throw new Error('Error al crear la persona');
  }

  return await response.json();
}


export async function updatePersona(id, personaData, token) {
  const response = await fetch(`${API_URL}/personas/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(personaData),
  });

  if (!response.ok) {
    throw new Error('Error al actualizar la persona');
  }

  return await response.json();
}


export async function deletePersona(id, token) {
  const response = await fetch(`${API_URL}/personas/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('Error al eliminar la persona');
  }

  return await response.json();
}