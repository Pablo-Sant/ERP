// src/pages/modules/ProjectManagement.jsx - VERSÃO MELHORADA
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import "../../styles/Module.css";

const ProjectManagement = () => {
  const { user } = useAuth();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get('/projects');
      
      // Verifique a estrutura dos dados retornados
      console.log('Dados dos projetos:', response.data);
      
      if (Array.isArray(response.data)) {
        setProjects(response.data);
      } else {
        setProjects([]);
        setError('Formato de dados inválido');
      }
    } catch (error) {
      console.error('Erro ao buscar projetos:', error);
      setError(`Erro: ${error.message || 'Não foi possível carregar os projetos'}`);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Não definida';
    try {
      return new Date(dateString).toLocaleDateString('pt-BR');
    } catch {
      return dateString;
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Carregando projetos...</p>
      </div>
    );
  }

  return (
    <div className="project-management">
      <header className="module-header">
        <h1>Gestão de Projetos</h1>
        <div className="user-info">
          <span className="welcome">Bem-vindo, <strong>{user?.nome || user?.email}</strong></span>
          <button onClick={fetchProjects} className="refresh-button">
            ↻ Atualizar
          </button>
        </div>
      </header>

      {error && (
        <div className="error-alert">
          <p>{error}</p>
          <button onClick={fetchProjects}>Tentar novamente</button>
        </div>
      )}

      <div className="projects-stats">
        <div className="stat-card">
          <span className="stat-number">{projects.length}</span>
          <span className="stat-label">Total de Projetos</span>
        </div>
        <div className="stat-card">
          <span className="stat-number">
            {projects.filter(p => p.status === 'EM_ANDAMENTO').length}
          </span>
          <span className="stat-label">Em Andamento</span>
        </div>
        <div className="stat-card">
          <span className="stat-number">
            {projects.filter(p => p.status === 'CONCLUIDO').length}
          </span>
          <span className="stat-label">Concluídos</span>
        </div>
      </div>

      <div className="projects-list">
        {projects.length > 0 ? (
          <div className="projects-grid">
            {projects.map(project => {
              // Use uma chave única baseada no que estiver disponível
              const projectKey = project.id_projeto || project.id || 
                               `${project.nome}-${project.created_at}`;
              
              return (
                <div 
                  key={projectKey}
                  className="project-card"
                >
                  <div className="project-header">
                    <h3 className="project-title">{project.nome}</h3>
                    <span className={`status-badge status-${(project.status || 'PLANEJAMENTO').toLowerCase()}`}>
                      {project.status || 'PLANEJAMENTO'}
                    </span>
                  </div>
                  
                  <p className="project-description">
                    {project.descricao || 'Sem descrição disponível.'}
                  </p>
                  
                  <div className="project-details">
                    <div className="detail-row">
                      <span className="detail-label">Início Previsto:</span>
                      <span className="detail-value">
                        {formatDate(project.data_inicio_prevista)}
                      </span>
                    </div>
                    
                    <div className="detail-row">
                      <span className="detail-label">Término Previsto:</span>
                      <span className="detail-value">
                        {formatDate(project.data_fim_prevista)}
                      </span>
                    </div>
                    
                    <div className="detail-row">
                      <span className="detail-label">Prioridade:</span>
                      <span className={`priority-badge priority-${(project.prioridade || 'MEDIA').toLowerCase()}`}>
                        {project.prioridade || 'MÉDIA'}
                      </span>
                    </div>
                    
                    {project.porcentagem_conclusao !== undefined && (
                      <div className="detail-row">
                        <span className="detail-label">Progresso:</span>
                        <div className="progress-bar">
                          <div 
                            className="progress-fill"
                            style={{ width: `${project.porcentagem_conclusao}%` }}
                          ></div>
                          <span className="progress-text">
                            {project.porcentagem_conclusao}%
                          </span>
                        </div>
                      </div>
                    )}
                    
                    <div className="detail-row">
                      <span className="detail-label">Orçamento:</span>
                      <span className="detail-value">
                        R$ {project.orcamento_total?.toLocaleString('pt-BR') || '0,00'}
                      </span>
                    </div>
                  </div>
                  
                  <div className="project-actions">
                    <button className="action-btn view-btn">Ver Detalhes</button>
                    <button className="action-btn edit-btn">Editar</button>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-icon">📁</div>
            <h3>Nenhum projeto encontrado</h3>
            <p>Não há projetos cadastrados no sistema.</p>
            <button className="create-project-btn">
              + Criar Novo Projeto
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectManagement;