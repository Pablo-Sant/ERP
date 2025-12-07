// src/pages/modules/Financial.jsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import "../../styles/Module.css";
import FinancialDashboard from '../../components/financial/FinancialDashboard';
import FinancialAccounts from '../../components/financial/FinancialAccounts';
import FinancialTransactions from '../../components/financial/FinancialTransactions';
import FinancialBudgets from '../../components/financial/FinancialBudgets';
import FinancialReports from '../../components/financial/FinancialReports';

const Financial = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Buscar dados do dashboard
  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await api.get('/fi/dashboard');
      setDashboardData(response.data);
      setError(null);
    } catch (error) {
      console.error('Erro ao carregar dashboard:', error);
      setError('Não foi possível carregar os dados financeiros');
    } finally {
      setLoading(false);
    }
  };

  // Buscar dados do relatório de receitas/despesas
  const fetchIncomeExpenseReport = async (startDate, endDate) => {
    try {
      const response = await api.get('/fi/relatorios/receitas-despesas', {
        params: {
          data_inicio: startDate,
          data_fim: endDate
        }
      });
      return response.data;
    } catch (error) {
      console.error('Erro ao carregar relatório:', error);
      throw error;
    }
  };

  // Carregar dados iniciais
  useEffect(() => {
    fetchDashboardData();
  }, []);

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'accounts', label: 'Contas', icon: '🏦' },
    { id: 'transactions', label: 'Transações', icon: '💳' },
    { id: 'budgets', label: 'Orçamentos', icon: '📋' },
    { id: 'reports', label: 'Relatórios', icon: '📈' },
    { id: 'invoices', label: 'Notas Fiscais', icon: '🧾' },
    { id: 'taxes', label: 'Impostos', icon: '💰' }
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <FinancialDashboard 
            data={dashboardData}
            loading={loading}
            error={error}
            onRefresh={fetchDashboardData}
          />
        );
      case 'accounts':
        return <FinancialAccounts />;
      case 'transactions':
        return <FinancialTransactions />;
      case 'budgets':
        return <FinancialBudgets />;
      case 'reports':
        return (
          <FinancialReports 
            onGenerateReport={fetchIncomeExpenseReport}
          />
        );
      case 'invoices':
        return <div className="card"><h3>Notas Fiscais</h3><p>Em desenvolvimento...</p></div>;
      case 'taxes':
        return <div className="card"><h3>Impostos</h3><p>Em desenvolvimento...</p></div>;
      default:
        return <div>Selecione uma opção</div>;
    }
  };

  return (
    <div className="financial-module">
      {/* Cabeçalho do Módulo */}
      <div className="module-fi-header">
        <div className="header-content">
          <h1>
            <span className="module-icon">💰</span>
            Módulo Financeiro
          </h1>
          <p className="module-subtitle">Gestão completa das finanças da empresa</p>
          
          <div className="module-user-info">
            <div className="user-role-badge">
              <span className="role-icon">👤</span>
              <span className="role-name">{user?.nome || 'Usuário'}</span>
              <span className="role-permission">Financeiro</span>
            </div>
            <div className="module-actions">
              <button 
                className="action-btn refresh-btn"
                onClick={fetchDashboardData}
                disabled={loading}
              >
                {loading ? '🔄 Atualizando...' : '🔄 Atualizar'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Navegação por Abas */}
      <div className="module-tabs">
        <div className="tabs-container">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <span className="tab-icon">{tab.icon}</span>
              <span className="tab-label">{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Conteúdo Principal */}
      <div className="module-content">
        {renderTabContent()}
      </div>

      {/* Rodapé */}
      <div className="module-footer">
        <div className="footer-info">
          <span className="timestamp">
            Última atualização: {new Date().toLocaleString('pt-BR')}
          </span>
          <span className="module-version">v1.0.0</span>
        </div>
        <div className="footer-links">
          <a href="/api/fi/health" target="_blank" rel="noopener noreferrer">
            🔍 Verificar Saúde da API
          </a>
          <a href="/docs#/Financeiro" target="_blank" rel="noopener noreferrer">
            📚 Documentação
          </a>
        </div>
      </div>
    </div>
  );
};

export default Financial;