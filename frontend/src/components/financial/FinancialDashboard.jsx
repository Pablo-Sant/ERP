// src/components/financial/FinancialDashboard.jsx
import React from 'react';
import "../../styles/Module.css";

const FinancialDashboard = ({ data, loading, error, onRefresh }) => {
  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Carregando dados financeiros...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <div className="error-icon">⚠️</div>
        <h3>Erro ao carregar dados</h3>
        <p>{error}</p>
        <button onClick={onRefresh} className="retry-btn">
          Tentar novamente
        </button>
      </div>
    );
  }

  if (!data) {
    return null;
  }

  const { estatisticas, ultimos_lancamentos, endpoints } = data;

  return (
    <div className="financial-dashboard">
      {/* Cards de Estatísticas */}
      <div className="dashboard-stats">
        <div className="stat-card total-revenue">
          <div className="stat-header">
            <span className="stat-icon">📈</span>
            <h3>Receitas do Mês</h3>
          </div>
          <div className="stat-value">
            R$ {estatisticas.receitas_mes?.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) || '0,00'}
          </div>
          <div className="stat-trend">
            <span className="trend-up">+12% vs mês anterior</span>
          </div>
        </div>

        <div className="stat-card total-expenses">
          <div className="stat-header">
            <span className="stat-icon">📉</span>
            <h3>Despesas do Mês</h3>
          </div>
          <div className="stat-value">
            R$ {estatisticas.despesas_mes?.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) || '0,00'}
          </div>
          <div className="stat-trend">
            <span className="trend-down">-5% vs mês anterior</span>
          </div>
        </div>

        <div className="stat-card total-balance">
          <div className="stat-header">
            <span className="stat-icon">💰</span>
            <h3>Saldo Total</h3>
          </div>
          <div className="stat-value">
            R$ {estatisticas.saldo_total?.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) || '0,00'}
          </div>
          <div className="stat-trend">
            <span className="trend-neutral">Atualizado</span>
          </div>
        </div>

        <div className="stat-card monthly-result">
          <div className="stat-header">
            <span className="stat-icon">📊</span>
            <h3>Resultado Mês</h3>
          </div>
          <div className="stat-value">
            R$ {estatisticas.resultado_mes?.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) || '0,00'}
          </div>
          <div className={`stat-trend ${estatisticas.resultado_mes >= 0 ? 'trend-up' : 'trend-down'}`}>
            {estatisticas.resultado_mes >= 0 ? '✅ Lucro' : '❌ Prejuízo'}
          </div>
        </div>
      </div>

      {/* Gráfico Simulado */}
      <div className="dashboard-chart">
        <div className="chart-header">
          <h3>Fluxo Mensal</h3>
          <div className="chart-legend">
            <span className="legend-item revenue">Receitas</span>
            <span className="legend-item expense">Despesas</span>
          </div>
        </div>
        <div className="chart-placeholder">
          <div className="chart-bars">
            {[1, 2, 3, 4, 5, 6].map(month => (
              <div key={month} className="chart-bar-container">
                <div 
                  className="chart-bar revenue-bar" 
                  style={{ height: `${30 + Math.random() * 50}%` }}
                ></div>
                <div 
                  className="chart-bar expense-bar" 
                  style={{ height: `${20 + Math.random() * 40}%` }}
                ></div>
              </div>
            ))}
          </div>
          <div className="chart-months">
            {['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'].map(month => (
              <span key={month} className="month-label">{month}</span>
            ))}
          </div>
        </div>
      </div>

      {/* Últimas Transações */}
      <div className="recent-transactions">
        <div className="transactions-header">
          <h3>Últimas Transações</h3>
          <a href={endpoints?.lancamentos} className="view-all-link">
            Ver todas →
          </a>
        </div>
        <div className="transactions-list">
          {ultimos_lancamentos?.slice(0, 5).map(transaction => (
            <div key={transaction.id} className="transaction-item">
              <div className="transaction-info">
                <div className="transaction-description">
                  <span className={`transaction-type ${transaction.tipo}`}>
                    {transaction.tipo === 'receita' ? '💰' : '💸'}
                  </span>
                  <span className="transaction-desc">{transaction.descricao}</span>
                </div>
                <div className="transaction-date">
                  {new Date(transaction.data).toLocaleDateString('pt-BR')}
                </div>
              </div>
              <div className={`transaction-value ${transaction.tipo}`}>
                R$ {transaction.valor?.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Resumo de Contas */}
      <div className="accounts-summary">
        <h3>Resumo de Contas</h3>
        <div className="accounts-grid">
          <div className="account-summary-card">
            <div className="account-type">Contas Ativas</div>
            <div className="account-count">{estatisticas.contas_ativas || 0}</div>
          </div>
          <div className="account-summary-card">
            <div className="account-type">Total de Contas</div>
            <div className="account-count">{estatisticas.total_contas || 0}</div>
          </div>
          <div className="account-summary-card">
            <div className="account-type">Lançamentos</div>
            <div className="account-count">{estatisticas.total_lancamentos || 0}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FinancialDashboard;