const API_URL = 'http://127.0.0.1:8090/api';

// Función centralizada para peticiones autenticadas
export async function apiFetch(endpoint, options = {}) {
  const token = localStorage.getItem('token');

  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Intercepción central de token expirado o inválido
  if (response.status === 401) {
    localStorage.removeItem('token');
    
    // Evita bucles infinitos si el 401 viene del mismo endpoint de login
    if (!endpoint.includes('/auth/login')) {
      window.location.href = '/login'; 
      throw new Error('Tu sesión ha expirado. Redirigiendo...');
    }
  }

  // Manejo de respuestas sin cuerpo (ej: 204 No Content en DELETE)
  if (response.status === 204) {
    return { success: true };
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || 'Ocurrió un error en la petición');
  }

  return data;
}




// --- AUTENTICACIÓN ---

export async function login(email, password) {
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

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Error al iniciar sesión');
  }

  return data; // Retorna { access_token, token_type }
}

export async function register(email, password) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Error al registrar usuario');
  }

  return data;
}

// --- GESTIÓN DE PERSONAS ---

export async function getPersonas(token) {
  const response = await fetch(`${API_URL}/personas`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    // Si la respuesta no es OK, muestra la razón exacta dada por FastAPI (ej. "Not authenticated")
    throw new Error(data.detail || 'Error al obtener la lista de personas');
  }

  return data;
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

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Error al crear la persona');
  }

  return data;
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

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Error al actualizar la persona');
  }

  return data;
}

export async function deletePersona(id, token) {
  const response = await fetch(`${API_URL}/personas/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Error al eliminar la persona');
  }

  // Si el backend responde con 204 (sin cuerpo), evita el error de parseo JSON
  if (response.status === 204) {
    return { success: true };
  }

  return await response.json();
}