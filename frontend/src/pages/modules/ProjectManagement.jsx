import React, { useState } from 'react';
import "../../styles/Module.css";

const ProjectManagement = () => {
  const [projects, setProjects] = useState([
    {
      id: 1,
      name: 'Implementação ERP',
      description: 'Implementação do sistema ERP na matriz',
      startDate: '2024-01-15',
      endDate: '2024-06-30',
      status: 'Em Andamento',
      manager: 'João Silva',
      budget: 'R$ 150.000'
    },
    {
      id: 2,
      name: 'Site Corporativo',
      description: 'Desenvolvimento do novo site institucional',
      startDate: '2024-02-01',
      endDate: '2024-03-15',
      status: 'Planejado',
      manager: 'Maria Santos',
      budget: 'R$ 45.000'
    }
  ]);

  const [newProject, setNewProject] = useState({
    name: '',
    description: '',
    startDate: '',
    endDate: '',
    status: 'Planejado',
    manager: '',
    budget: ''
  });

  const addProject = () => {
    if (newProject.name && newProject.description) {
      const project = {
        ...newProject,
        id: Date.now()
      };
      setProjects([...projects, project]);
      setNewProject({
        name: '',
        description: '',
        startDate: '',
        endDate: '',
        status: 'Planejado',
        manager: '',
        budget: ''
      });
    }
  };

  const deleteProject = (id) => {
    setProjects(projects.filter(project => project.id !== id));
  };

  return (
    <div className="module">
      <div className="module-header">
        <h1>Gestão de Projetos</h1>
        <p>Planejamento e controle de projetos</p>
      </div>

      <div className="module-content">
        <div className="card">
          <h2>Novo Projeto</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Nome do Projeto</label>
              <input
                type="text"
                value={newProject.name}
                onChange={(e) => setNewProject({...newProject, name: e.target.value})}
                placeholder="Digite o nome do projeto"
              />
            </div>
            <div className="form-group">
              <label>Descrição</label>
              <input
                type="text"
                value={newProject.description}
                onChange={(e) => setNewProject({...newProject, description: e.target.value})}
                placeholder="Descrição do projeto"
              />
            </div>
            <div className="form-group">
              <label>Data Início</label>
              <input
                type="date"
                value={newProject.startDate}
                onChange={(e) => setNewProject({...newProject, startDate: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Data Término</label>
              <input
                type="date"
                value={newProject.endDate}
                onChange={(e) => setNewProject({...newProject, endDate: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Status</label>
              <select
                value={newProject.status}
                onChange={(e) => setNewProject({...newProject, status: e.target.value})}
              >
                <option value="Planejado">Planejado</option>
                <option value="Em Andamento">Em Andamento</option>
                <option value="Concluído">Concluído</option>
                <option value="Cancelado">Cancelado</option>
              </select>
            </div>
            <div className="form-group">
              <label>Gerente</label>
              <input
                type="text"
                value={newProject.manager}
                onChange={(e) => setNewProject({...newProject, manager: e.target.value})}
                placeholder="Responsável pelo projeto"
              />
            </div>
            <div className="form-group">
              <label>Orçamento</label>
              <input
                type="text"
                value={newProject.budget}
                onChange={(e) => setNewProject({...newProject, budget: e.target.value})}
                placeholder="Valor do orçamento"
              />
            </div>
            <div className="form-group">
              <button onClick={addProject} className="btn btn-primary">
                Adicionar Projeto
              </button>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Projetos</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Descrição</th>
                  <th>Início</th>
                  <th>Término</th>
                  <th>Status</th>
                  <th>Gerente</th>
                  <th>Orçamento</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {projects.map(project => (
                  <tr key={project.id}>
                    <td><strong>{project.name}</strong></td>
                    <td>{project.description}</td>
                    <td>{project.startDate}</td>
                    <td>{project.endDate}</td>
                    <td>
                      <span className={`status-badge status-${project.status.toLowerCase().replace(' ', '-')}`}>
                        {project.status}
                      </span>
                    </td>
                    <td>{project.manager}</td>
                    <td>{project.budget}</td>
                    <td>
                      <button 
                        onClick={() => deleteProject(project.id)}
                        className="btn btn-danger btn-sm"
                      >
                        Excluir
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectManagement;