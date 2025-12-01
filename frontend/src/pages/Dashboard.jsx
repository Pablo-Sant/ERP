// src/pages/Dashboard.jsx
import React from 'react';
import { useAuth } from '../hooks/useAuth';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const { user } = useAuth();

  const stats = [
    { title: 'Projetos Ativos', value: '12', icon: '📋', color: '#3498db' },
    { title: 'Itens em Estoque', value: '245', icon: '📦', color: '#2ecc71' },
    { title: 'Vendas do Mês', value: 'R$ 48.250', icon: '💰', color: '#9b59b6' },
    { title: 'Tickets Abertos', value: '8', icon: '🔧', color: '#e74c3c' }
  ];

  const recentActivities = [
    { action: 'Novo projeto criado', module: 'PS', time: '5 min atrás' },
    { action: 'Item adicionado ao estoque', module: 'MM', time: '12 min atrás' },
    { action: 'Venda realizada', module: 'VC', time: '1 hora atrás' },
    { action: 'Relatório gerado', module: 'BI', time: '2 horas atrás' }
  ];

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Bem-vindo de volta, <strong>{user?.nome}</strong>! 👋</p>
      </div>

      <div className="stats-grid">
        {stats.map((stat, index) => (
          <div key={index} className="stat-card">
            <div className="stat-icon" style={{ backgroundColor: stat.color }}>
              {stat.icon}
            </div>
            <div className="stat-info">
              <h3>{stat.value}</h3>
              <p>{stat.title}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="dashboard-content">
        <div className="dashboard-card">
          <h2>Atividades Recentes</h2>
          <div className="activities-list">
            {recentActivities.map((activity, index) => (
              <div key={index} className="activity-item">
                <div className="activity-content">
                  <span className="activity-action">{activity.action}</span>
                  <span className="activity-module">{activity.module}</span>
                </div>
                <span className="activity-time">{activity.time}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="dashboard-card">
          <h2>Módulos do Sistema</h2>
          <div className="modules-grid">
            <div className="module-quick">
              <span className="module-icon">📋</span>
              <span className="module-name">Gestão de Projetos</span>
            </div>
            <div className="module-quick">
              <span className="module-icon">📦</span>
              <span className="module-name">Gestão de Materiais</span>
            </div>
            <div className="module-quick">
              <span className="module-icon">💰</span>
              <span className="module-name">Financeiro</span>
            </div>
            <div className="module-quick">
              <span className="module-icon">🏢</span>
              <span className="module-name">Gestão de Ativos</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;