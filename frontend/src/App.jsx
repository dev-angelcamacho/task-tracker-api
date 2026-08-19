import { useState, useEffect } from 'react';
import Login from './components/Login';
import Personas from './components/Personas';

function App() {
  const [token, setToken] = useState(null);

  useEffect(() => {
    // Al cargar la app, verificar si ya existe un token en localStorage
    const savedToken = localStorage.getItem('token');
    if (savedToken) {
      setToken(savedToken);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <div className="container mt-4">
      {!token ? (
        <Login onLoginSuccess={(newToken) => setToken(newToken)} />
      ) : (
        /* 👇 AQUÍ REEMPLAZAMOS EL DIV DE PRUEBA POR EL COMPONENTE PERSONAS */
        <Personas token={token} onLogout={handleLogout} />
      )}
    </div>
  );
}

export default App;