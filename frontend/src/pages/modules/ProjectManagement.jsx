// src/pages/modules/ProjectManagement.jsx
import React, { useState, useEffect } from 'react'; // ← ADICIONE useState e useEffect
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import "../../styles/Module.css";

const ProjectManagement = () => {
  const { user } = useAuth();
  const [projects, setProjects] = useState([]); // ← Agora useState está definido
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await api.get('/projects');
      setProjects(response.data);
    } catch (error) {
      console.error('Erro ao buscar projetos:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Carregando projetos...</div>;
  }

  return (
    <div className="project-management">
      <h1>Gestão de Projetos</h1>
      <p>Bem-vindo, {user?.nome}</p>
      <div className="projects-list">
        {projects.length > 0 ? (
          projects.map(project => (
            <div key={project.id} className="project-card">
              <h3>{project.nome}</h3>
              <p>{project.descricao}</p>
            </div>
          ))
        ) : (
          <p>Nenhum projeto encontrado</p>
        )}
      </div>
    </div>
  );
};

export default ProjectManagement;