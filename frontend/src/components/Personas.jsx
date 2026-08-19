import { useState, useEffect } from 'react';
import { getPersonas, createPersona, updatePersona, deletePersona } from '../services/api';

function Personas({ token, onLogout }) {
  const [personas, setPersonas] = useState([]);
  const [name, setName] = useState('');
  const [lastname, setLastname] = useState('');
  const [phone, setPhone] = useState('');
  const [editingId, setEditingId] = useState(null); // null = Modo Creación, ID = Modo Edición
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    cargarPersonas();
  }, []);

  const cargarPersonas = async () => {
    try {
      const data = await getPersonas(token);
      setPersonas(data);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleEditClick = (persona) => {
    setEditingId(persona.id);
    setName(persona.name);
    setLastname(persona.lastname);
    setPhone(persona.phone);
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setName('');
    setLastname('');
    setPhone('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const personaData = {
        name,
        lastname,
        phone: parseInt(phone, 10),
        is_actived: true,
      };

      if (editingId) {
        // Ejecutar actualización (PUT)
        await updatePersona(editingId, personaData, token);
      } else {
        // Ejecutar creación (POST)
        await createPersona(personaData, token);
      }

      handleCancelEdit(); // Limpiar formulario y salir de modo edición
      cargarPersonas(); // Recargar la lista
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Seguro que deseas eliminar esta persona?')) return;

    try {
      await deletePersona(id, token);
      cargarPersonas();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="row g-4">
      {/* Encabezado */}
      <div className="d-flex justify-content-between align-items-center mb-2">
        <h2>Gestión de Personas</h2>
        <button className="btn btn-outline-danger btn-sm" onClick={onLogout}>
          Cerrar Sesión
        </button>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {/* Formulario Dinámico (Crear / Editar) */}
      <div className="col-md-4">
        <div className="card shadow-sm p-3">
          <h5 className="card-title mb-3">
            {editingId ? 'Editar Persona' : 'Agregar Persona'}
          </h5>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label">Nombre</label>
              <input
                type="text"
                className="form-control"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Apellido</label>
              <input
                type="text"
                className="form-control"
                value={lastname}
                onChange={(e) => setLastname(e.target.value)}
                required
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Teléfono</label>
              <input
                type="number"
                className="form-control"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                required
              />
            </div>

            <button
              type="submit"
              className={`btn w-100 ${editingId ? 'btn-warning' : 'btn-success'}`}
              disabled={loading}
            >
              {loading
                ? 'Guardando...'
                : editingId
                ? 'Actualizar Persona'
                : 'Guardar Persona'}
            </button>

            {editingId && (
              <button
                type="button"
                className="btn btn-link text-secondary w-100 mt-2"
                onClick={handleCancelEdit}
              >
                Cancelar Edición
              </button>
            )}
          </form>
        </div>
      </div>

      {/* Tabla de resultados */}
      <div className="col-md-8">
        <div className="card shadow-sm p-3">
          <h5 className="card-title mb-3">Lista de Personas</h5>
          {personas.length === 0 ? (
            <p className="text-muted">No hay personas registradas.</p>
          ) : (
            <table className="table table-hover align-middle">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre</th>
                  <th>Apellido</th>
                  <th>Teléfono</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {personas.map((p) => (
                  <tr key={p.id}>
                    <td>{p.id}</td>
                    <td>{p.name}</td>
                    <td>{p.lastname}</td>
                    <td>{p.phone}</td>
                    <td>
                      <button
                        className="btn btn-warning btn-sm me-2"
                        onClick={() => handleEditClick(p)}
                      >
                        Editar
                      </button>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => handleDelete(p.id)}
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

export default Personas;