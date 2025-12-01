import React, { useState } from 'react';
import "../../styles/Module.css";

const BusinessIntelligence = () => {
  const [reports, setReports] = useState([
    {
      id: 1,
      name: 'Relatório de Vendas Mensal',
      type: 'Vendas',
      description: 'Análise detalhada das vendas do mês',
      frequency: 'Mensal',
      lastRun: '2024-01-01',
      status: 'Ativo'
    },
    {
      id: 2,
      name: 'Dashboard Financeiro',
      type: 'Financeiro',
      description: 'Visão geral da saúde financeira',
      frequency: 'Diário',
      lastRun: '2024-01-05',
      status: 'Ativo'
    },
    {
      id: 3,
      name: 'Análise de Estoque',
      type: 'Estoque',
      description: 'Controle de giro e reposição',
      frequency: 'Semanal',
      lastRun: '2024-01-03',
      status: 'Inativo'
    }
  ]);

  const [kpis, setKpis] = useState([
    { name: 'Faturamento Mensal', value: 'R$ 245.680', trend: 'up', change: '+12%' },
    { name: 'Ticket Médio', value: 'R$ 1.245', trend: 'up', change: '+5%' },
    { name: 'Clientes Ativos', value: '156', trend: 'up', change: '+8%' },
    { name: 'Custos Operacionais', value: 'R$ 98.450', trend: 'down', change: '-3%' }
  ]);

  const [newReport, setNewReport] = useState({
    name: '',
    type: '',
    description: '',
    frequency: 'Mensal',
    status: 'Ativo'
  });

  const addReport = () => {
    if (newReport.name && newReport.type) {
      const report = {
        ...newReport,
        id: Date.now(),
        lastRun: new Date().toISOString().split('T')[0]
      };
      setReports([...reports, report]);
      setNewReport({
        name: '',
        type: '',
        description: '',
        frequency: 'Mensal',
        status: 'Ativo'
      });
    }
  };

  const deleteReport = (id) => {
    setReports(reports.filter(report => report.id !== id));
  };

  const runReport = (id) => {
    setReports(reports.map(report => 
      report.id === id 
        ? { ...report, lastRun: new Date().toISOString().split('T')[0] }
        : report
    ));
    alert('Relatório executado com sucesso!');
  };

  return (
    <div className="module">
      <div className="module-header">
        <h1>Business Intelligence</h1>
        <p>Relatórios e analytics</p>
      </div>

      <div className="module-content">
        <div className="bi-dashboard">
          <h2>KPIs Principais</h2>
          <div className="kpi-grid">
            {kpis.map((kpi, index) => (
              <div key={index} className="kpi-card">
                <div className="kpi-header">
                  <h3>{kpi.name}</h3>
                  <span className={`trend trend-${kpi.trend}`}>
                    {kpi.change}
                  </span>
                </div>
                <div className="kpi-value">{kpi.value}</div>
                <div className="kpi-trend">
                  {kpi.trend === 'up' ? '📈' : '📉'} 
                  {kpi.trend === 'up' ? ' Crescimento' : ' Redução'}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h2>Novo Relatório</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Nome do Relatório</label>
              <input
                type="text"
                value={newReport.name}
                onChange={(e) => setNewReport({...newReport, name: e.target.value})}
                placeholder="Nome do relatório"
              />
            </div>
            <div className="form-group">
              <label>Tipo</label>
              <select
                value={newReport.type}
                onChange={(e) => setNewReport({...newReport, type: e.target.value})}
              >
                <option value="">Selecione...</option>
                <option value="Vendas">Vendas</option>
                <option value="Financeiro">Financeiro</option>
                <option value="Estoque">Estoque</option>
                <option value="RH">Recursos Humanos</option>
                <option value="Projetos">Projetos</option>
                <option value="Clientes">Clientes</option>
              </select>
            </div>
            <div className="form-group full-width">
              <label>Descrição</label>
              <textarea
                value={newReport.description}
                onChange={(e) => setNewReport({...newReport, description: e.target.value})}
                placeholder="Descrição do relatório"
                rows="2"
              />
            </div>
            <div className="form-group">
              <label>Frequência</label>
              <select
                value={newReport.frequency}
                onChange={(e) => setNewReport({...newReport, frequency: e.target.value})}
              >
                <option value="Diário">Diário</option>
                <option value="Semanal">Semanal</option>
                <option value="Mensal">Mensal</option>
                <option value="Trimestral">Trimestral</option>
                <option value="Anual">Anual</option>
              </select>
            </div>
            <div className="form-group">
              <label>Status</label>
              <select
                value={newReport.status}
                onChange={(e) => setNewReport({...newReport, status: e.target.value})}
              >
                <option value="Ativo">Ativo</option>
                <option value="Inativo">Inativo</option>
              </select>
            </div>
            <div className="form-group">
              <button onClick={addReport} className="btn btn-primary">
                Criar Relatório
              </button>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Relatórios Disponíveis</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Tipo</th>
                  <th>Descrição</th>
                  <th>Frequência</th>
                  <th>Última Execução</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {reports.map(report => (
                  <tr key={report.id}>
                    <td><strong>{report.name}</strong></td>
                    <td>
                      <span className={`type-badge type-${report.type.toLowerCase()}`}>
                        {report.type}
                      </span>
                    </td>
                    <td>{report.description}</td>
                    <td>{report.frequency}</td>
                    <td>{report.lastRun}</td>
                    <td>
                      <span className={`status-badge status-${report.status.toLowerCase()}`}>
                        {report.status}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button 
                          onClick={() => runReport(report.id)}
                          className="btn btn-primary btn-sm"
                        >
                          Executar
                        </button>
                        <button 
                          onClick={() => deleteReport(report.id)}
                          className="btn btn-danger btn-sm"
                        >
                          Excluir
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <h2>Visualizações</h2>
          <div className="charts-grid">
            <div className="chart-placeholder">
              <h4>Faturamento Mensal</h4>
              <div className="chart-content">
                <p>📊 Gráfico de linha mostrando o faturamento dos últimos 12 meses</p>
              </div>
            </div>
            <div className="chart-placeholder">
              <h4>Distribuição de Vendas por Região</h4>
              <div className="chart-content">
                <p>🗺️ Mapa de calor com performance por região</p>
              </div>
            </div>
            <div className="chart-placeholder">
              <h4>Produtos Mais Vendidos</h4>
              <div className="chart-content">
                <p>📈 Gráfico de barras com top 10 produtos</p>
              </div>
            </div>
            <div className="chart-placeholder">
              <h4>Satisfação do Cliente</h4>
              <div className="chart-content">
                <p>⭐ Métricas de NPS e satisfação</p>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Exportar Dados</h2>
          <div className="export-options">
            <button className="btn btn-secondary">
              📥 Exportar para Excel
            </button>
            <button className="btn btn-secondary">
              📊 Exportar para PDF
            </button>
            <button className="btn btn-secondary">
              📋 Exportar para CSV
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BusinessIntelligence;