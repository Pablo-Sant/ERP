import React, { useState, useEffect } from 'react';
import axios from 'axios';
import "../../styles/Module.css";

const BusinessIntelligence = () => {
  const [reports, setReports] = useState([]);
  const [kpis, setKpis] = useState([]);
  const [dashboards, setDashboards] = useState([]);
  const [tendenciaData, setTendenciaData] = useState([]);
  const [loading, setLoading] = useState({
    kpis: false,
    reports: false,
    dashboards: false
  });
  const [selectedKpi, setSelectedKpi] = useState('vendas');
  const [selectedPeriodo, setSelectedPeriodo] = useState('mensal');
  const [exportData, setExportData] = useState([]);

  const API_URL = 'http://localhost:8000/api/bi';

  // Buscar KPIs principais
  const fetchKpis = async () => {
    setLoading(prev => ({ ...prev, kpis: true }));
    try {
      const response = await axios.get(`${API_URL}/kpis/calculados`);
      const kpiData = response.data.kpis;
      
      // Formatando KPIs para o frontend
      const formattedKpis = [
        { 
          name: 'Faturamento Total', 
          value: `R$ ${kpiData.total_vendas.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
          trend: kpiData.total_vendas > 0 ? 'up' : 'down',
          change: 'Total acumulado'
        },
        { 
          name: 'Ticket Médio', 
          value: `R$ ${kpiData.ticket_medio.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
          trend: kpiData.ticket_medio > 0 ? 'up' : 'down',
          change: 'Média por compra'
        },
        { 
          name: 'Clientes Ativos', 
          value: kpiData.total_clientes.toString(),
          trend: 'up',
          change: 'Clientes cadastrados'
        },
        { 
          name: 'Tickets Abertos', 
          value: kpiData.tickets_abertos.toString(),
          trend: kpiData.tickets_abertos > 0 ? 'down' : 'up',
          change: 'Aguardando atendimento'
        },
        { 
          name: 'Vendas Mês Atual', 
          value: `R$ ${kpiData.vendas_mes_atual.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
          trend: kpiData.vendas_mes_atual > 0 ? 'up' : 'down',
          change: 'Mês atual'
        },
        { 
          name: 'Taxa Resolução', 
          value: `${kpiData.taxa_resolucao_tickets.toFixed(1)}%`,
          trend: kpiData.taxa_resolucao_tickets > 80 ? 'up' : 'down',
          change: 'Últimos 30 dias'
        }
      ];
      setKpis(formattedKpis);
    } catch (error) {
      console.error('Erro ao buscar KPIs:', error);
      // Fallback para dados estáticos se a API falhar
      setKpis([
        { name: 'Faturamento Mensal', value: 'R$ 245.680', trend: 'up', change: '+12%' },
        { name: 'Ticket Médio', value: 'R$ 1.245', trend: 'up', change: '+5%' },
        { name: 'Clientes Ativos', value: '156', trend: 'up', change: '+8%' },
        { name: 'Custos Operacionais', value: 'R$ 98.450', trend: 'down', change: '-3%' }
      ]);
    } finally {
      setLoading(prev => ({ ...prev, kpis: false }));
    }
  };

  // Buscar dashboards
  const fetchDashboards = async () => {
    setLoading(prev => ({ ...prev, dashboards: true }));
    try {
      const response = await axios.get(`${API_URL}/dashboards/`);
      setDashboards(response.data);
    } catch (error) {
      console.error('Erro ao buscar dashboards:', error);
    } finally {
      setLoading(prev => ({ ...prev, dashboards: false }));
    }
  };

  // Buscar tendência de KPIs
  const fetchTendencia = async (kpi, periodo) => {
    try {
      const response = await axios.get(`${API_URL}/kpis/tendencia`, {
        params: { kpi, periodo }
      });
      setTendenciaData(response.data.tendencia || []);
    } catch (error) {
      console.error('Erro ao buscar tendência:', error);
    }
  };

  // Executar relatório predefinido
  const runPredefinedReport = async (reportType) => {
    try {
      let endpoint = '';
      let params = {};
      
      switch(reportType) {
        case 'vendas_vendedor':
          endpoint = `${API_URL}/relatorios/vendas-por-vendedor`;
          break;
        case 'vendas_mensais':
          endpoint = `${API_URL}/relatorios/vendas-mensais`;
          params = { meses: 12 };
          break;
        case 'clientes_ativos':
          endpoint = `${API_URL}/relatorios/clientes-ativos`;
          params = { top_n: 10 };
          break;
        case 'tickets_tipo':
          endpoint = `${API_URL}/relatorios/tickets-por-tipo`;
          break;
        default:
          return;
      }
      
      const response = await axios.get(endpoint, { params });
      setExportData(response.data.dados || []);
      alert(`Relatório ${reportType} executado! ${response.data.total_registros || 0} registros encontrados.`);
    } catch (error) {
      console.error('Erro ao executar relatório:', error);
      alert('Erro ao executar relatório: ' + error.message);
    }
  };

  // Exportar dados
  const exportDataToFormat = async (formato, tipo) => {
    try {
      const response = await axios.get(`${API_URL}/exportar/dados`, {
        params: { formato, tipo }
      });
      
      if (formato === 'csv') {
        // Criar arquivo CSV para download
        const blob = new Blob([response.data.dados], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${tipo}_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } else {
        // Para JSON, podemos mostrar em uma nova janela
        setExportData(response.data.dados);
        alert(`Dados exportados em ${formato.toUpperCase()}. Total: ${response.data.total_registros} registros.`);
      }
    } catch (error) {
      console.error('Erro ao exportar dados:', error);
      alert('Erro ao exportar dados: ' + error.message);
    }
  };

  // Executar query SQL customizada
  const executeCustomQuery = async (sqlQuery) => {
    try {
      const response = await axios.get(`${API_URL}/relatorios/executar`, {
        params: { 
          sql_query: sqlQuery,
          usar_cache: true 
        }
      });
      setExportData(response.data.dados || []);
      alert(`Query executada! ${response.data.total_registros || 0} registros retornados.`);
    } catch (error) {
      console.error('Erro ao executar query:', error);
      alert('Erro ao executar query: ' + error.message);
    }
  };

  // Buscar dados de dashboard específico
  const fetchDashboardData = async (dashboardId, atualizarCache = false) => {
    try {
      const response = await axios.get(`${API_URL}/dashboards/${dashboardId}/dados`, {
        params: { atualizar_cache: atualizarCache }
      });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar dados do dashboard:', error);
      return null;
    }
  };

  // Carregar dados iniciais
  useEffect(() => {
    fetchKpis();
    fetchDashboards();
    fetchTendencia(selectedKpi, selectedPeriodo);
  }, []);

  // Atualizar tendência quando seleção mudar
  useEffect(() => {
    if (selectedKpi && selectedPeriodo) {
      fetchTendencia(selectedKpi, selectedPeriodo);
    }
  }, [selectedKpi, selectedPeriodo]);

  return (
    <div className="module">
      <div className="module-header">
        <h1>Business Intelligence</h1>
        <p>Relatórios e analytics em tempo real</p>
      </div>

      <div className="module-content">
        {/* Seção de KPIs */}
        <div className="bi-dashboard">
          <div className="section-header">
            <h2>KPIs Principais</h2>
            <button 
              onClick={fetchKpis}
              className="btn btn-secondary btn-sm"
              disabled={loading.kpis}
            >
              {loading.kpis ? 'Atualizando...' : '🔄 Atualizar'}
            </button>
          </div>
          
          <div className="kpi-grid">
            {loading.kpis ? (
              <div className="loading">Carregando KPIs...</div>
            ) : (
              kpis.map((kpi, index) => (
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
                    {kpi.trend === 'up' ? ' Positivo' : ' Negativo'}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Seção de Análise de Tendência */}
        <div className="card">
          <div className="section-header">
            <h2>Análise de Tendência</h2>
            <div className="filter-controls">
              <select 
                value={selectedKpi}
                onChange={(e) => setSelectedKpi(e.target.value)}
                className="form-control-sm"
              >
                <option value="vendas">Vendas</option>
                <option value="tickets">Tickets</option>
                <option value="clientes">Clientes</option>
              </select>
              <select 
                value={selectedPeriodo}
                onChange={(e) => setSelectedPeriodo(e.target.value)}
                className="form-control-sm"
              >
                <option value="mensal">Mensal</option>
                <option value="diario">Diário</option>
                <option value="semanal">Semanal</option>
              </select>
            </div>
          </div>
          
          {tendenciaData.length > 0 ? (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Período</th>
                    <th>Quantidade</th>
                    <th>Valor Total</th>
                    <th>Resolvidos</th>
                  </tr>
                </thead>
                <tbody>
                  {tendenciaData.map((item, index) => (
                    <tr key={index}>
                      <td>{new Date(item.periodo).toLocaleDateString('pt-BR')}</td>
                      <td>{item.quantidade}</td>
                      <td>
                        {item.valor ? `R$ ${item.valor.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}` : 'N/A'}
                      </td>
                      <td>{item.resolvidos || 'N/A'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p>Nenhum dado de tendência disponível</p>
          )}
        </div>

        {/* Seção de Relatórios Predefinidos */}
        <div className="card">
          <h2>Relatórios Predefinidos</h2>
          <div className="reports-grid">
            <div className="report-card">
              <h4>Vendas por Vendedor</h4>
              <p>Total de vendas agrupadas por vendedor</p>
              <button 
                onClick={() => runPredefinedReport('vendas_vendedor')}
                className="btn btn-primary btn-sm"
              >
                Executar Relatório
              </button>
            </div>
            
            <div className="report-card">
              <h4>Vendas Mensais</h4>
              <p>Vendas totais por mês</p>
              <button 
                onClick={() => runPredefinedReport('vendas_mensais')}
                className="btn btn-primary btn-sm"
              >
                Executar Relatório
              </button>
            </div>
            
            <div className="report-card">
              <h4>Clientes Mais Ativos</h4>
              <p>Top 10 clientes com mais compras</p>
              <button 
                onClick={() => runPredefinedReport('clientes_ativos')}
                className="btn btn-primary btn-sm"
              >
                Executar Relatório
              </button>
            </div>
            
            <div className="report-card">
              <h4>Tickets por Tipo</h4>
              <p>Distribuição de tickets por tipo</p>
              <button 
                onClick={() => runPredefinedReport('tickets_tipo')}
                className="btn btn-primary btn-sm"
              >
                Executar Relatório
              </button>
            </div>
          </div>
        </div>

        {/* Seção de Dashboards */}
        <div className="card">
          <div className="section-header">
            <h2>Dashboards Disponíveis</h2>
            <button 
              onClick={fetchDashboards}
              className="btn btn-secondary btn-sm"
              disabled={loading.dashboards}
            >
              {loading.dashboards ? 'Carregando...' : '🔄 Atualizar'}
            </button>
          </div>
          
          {loading.dashboards ? (
            <p>Carregando dashboards...</p>
          ) : dashboards.length > 0 ? (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Descrição</th>
                    <th>Última Atualização</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {dashboards.map(dashboard => (
                    <tr key={dashboard.id_dashboard}>
                      <td><strong>{dashboard.nome}</strong></td>
                      <td>{dashboard.descricao}</td>
                      <td>{new Date(dashboard.data_atualizacao).toLocaleDateString('pt-BR')}</td>
                      <td>
                        <div className="action-buttons">
                          <button 
                            onClick={() => fetchDashboardData(dashboard.id_dashboard, false)}
                            className="btn btn-primary btn-sm"
                          >
                            Ver Dados
                          </button>
                          <button 
                            onClick={() => fetchDashboardData(dashboard.id_dashboard, true)}
                            className="btn btn-secondary btn-sm"
                          >
                            Atualizar Cache
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p>Nenhum dashboard disponível</p>
          )}
        </div>

        {/* Seção de Exportação de Dados */}
        <div className="card">
          <h2>Exportar Dados</h2>
          <div className="export-section">
            <div className="export-controls">
              <select id="exportType" className="form-control">
                <option value="vendas">Vendas</option>
                <option value="clientes">Clientes</option>
                <option value="tickets">Tickets</option>
              </select>
              
              <select id="exportFormat" className="form-control">
                <option value="json">JSON</option>
                <option value="csv">CSV</option>
              </select>
              
              <button 
                onClick={() => {
                  const tipo = document.getElementById('exportType').value;
                  const formato = document.getElementById('exportFormat').value;
                  exportDataToFormat(formato, tipo);
                }}
                className="btn btn-primary"
              >
                Exportar Dados
              </button>
            </div>
            
            <div className="export-options">
              <button 
                onClick={() => exportDataToFormat('csv', 'vendas')}
                className="btn btn-secondary"
              >
                📥 Exportar Vendas para CSV
              </button>
              <button 
                onClick={() => exportDataToFormat('csv', 'clientes')}
                className="btn btn-secondary"
              >
                📊 Exportar Clientes para CSV
              </button>
              <button 
                onClick={() => exportDataToFormat('json', 'tickets')}
                className="btn btn-secondary"
              >
                📋 Exportar Tickets para JSON
              </button>
            </div>
          </div>
        </div>

        {/* Seção de Query SQL Customizada */}
        <div className="card">
          <h2>Consulta SQL Customizada</h2>
          <div className="sql-query-section">
            <div className="form-group">
              <label>Digite sua query SQL (somente SELECT):</label>
              <textarea 
                id="sqlQuery"
                className="form-control"
                rows="4"
                placeholder="SELECT * FROM vc.vendedor LIMIT 10"
                defaultValue="SELECT v.nome as vendedor, COUNT(p.pedidoid) as total_pedidos FROM vc.vendedor v LEFT JOIN vc.pedidos_de_venda p ON v.vendedorid = p.vendedorid GROUP BY v.vendedorid, v.nome ORDER BY total_pedidos DESC LIMIT 5"
              />
            </div>
            <button 
              onClick={() => {
                const query = document.getElementById('sqlQuery').value;
                executeCustomQuery(query);
              }}
              className="btn btn-primary"
            >
              Executar Query
            </button>
          </div>
        </div>

        {/* Visualização de Dados Exportados */}
        {exportData.length > 0 && (
          <div className="card">
            <div className="section-header">
              <h2>Dados Exportados ({exportData.length} registros)</h2>
              <button 
                onClick={() => setExportData([])}
                className="btn btn-danger btn-sm"
              >
                Limpar
              </button>
            </div>
            
            <div className="table-container" style={{ maxHeight: '400px', overflowY: 'auto' }}>
              <table>
                <thead>
                  <tr>
                    {exportData[0] && Object.keys(exportData[0]).map((key, index) => (
                      <th key={index}>{key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {exportData.slice(0, 50).map((row, rowIndex) => (
                    <tr key={rowIndex}>
                      {Object.values(row).map((value, colIndex) => (
                        <td key={colIndex}>
                          {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
              {exportData.length > 50 && (
                <p className="text-muted">Mostrando 50 de {exportData.length} registros</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BusinessIntelligence;