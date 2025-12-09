import React, { useState, useEffect } from 'react';
import biAPI from '../../services/biAPI'; // Importando a API criada
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
  const [kpiList, setKpiList] = useState([]); // Lista de KPIs do sistema
  const [selectedDashboard, setSelectedDashboard] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);

  // Buscar KPIs principais do sistema
  const fetchKpis = async () => {
    setLoading(prev => ({ ...prev, kpis: true }));
    try {
      const response = await biAPI.getKPIs({ 
        tipo: 'principal',
        ativos: true 
      });
      
      if (response && response.length > 0) {
        setKpiList(response);
        
        // Formatando KPIs para o frontend
        const formattedKpis = response.slice(0, 6).map(kpi => {
          let value = '';
          let trend = 'neutral';
          
          if (kpi.tipo_medida === 'monetario') {
            value = biAPI.formatCurrency(kpi.valor_atual || 0);
            trend = (kpi.variacao_percentual || 0) >= 0 ? 'up' : 'down';
          } else if (kpi.tipo_medida === 'percentual') {
            value = biAPI.formatPercentage(kpi.valor_atual || 0);
            trend = (kpi.valor_atual || 0) >= (kpi.meta || 0) ? 'up' : 'down';
          } else {
            value = biAPI.formatNumber(kpi.valor_atual || 0);
            trend = (kpi.variacao_percentual || 0) >= 0 ? 'up' : 'down';
          }
          
          return {
            id: kpi.id,
            name: kpi.nome,
            value: value,
            trend: trend,
            change: kpi.variacao_percentual ? 
              `${kpi.variacao_percentual >= 0 ? '+' : ''}${kpi.variacao_percentual.toFixed(1)}%` : 
              'N/A',
            description: kpi.descricao
          };
        });
        
        setKpis(formattedKpis);
      } else {
        // Fallback para dados estáticos se não houver KPIs
        setKpis(getFallbackKpis());
      }
    } catch (error) {
      console.error('Erro ao buscar KPIs:', error);
      // Fallback para dados estáticos se a API falhar
      setKpis(getFallbackKpis());
    } finally {
      setLoading(prev => ({ ...prev, kpis: false }));
    }
  };

  // Função para KPIs fallback
  const getFallbackKpis = () => [
    { 
      id: 1, 
      name: 'Faturamento Mensal', 
      value: biAPI.formatCurrency(245680), 
      trend: 'up', 
      change: '+12%',
      description: 'Faturamento total do mês' 
    },
    { 
      id: 2, 
      name: 'Ticket Médio', 
      value: biAPI.formatCurrency(1245), 
      trend: 'up', 
      change: '+5%',
      description: 'Valor médio por compra' 
    },
    { 
      id: 3, 
      name: 'Clientes Ativos', 
      value: '156', 
      trend: 'up', 
      change: '+8%',
      description: 'Clientes com atividade recente' 
    },
    { 
      id: 4, 
      name: 'Custos Operacionais', 
      value: biAPI.formatCurrency(98450), 
      trend: 'down', 
      change: '-3%',
      description: 'Custos totais operacionais' 
    },
    { 
      id: 5, 
      name: 'Taxa Conversão', 
      value: biAPI.formatPercentage(23.5), 
      trend: 'up', 
      change: '+2.1%',
      description: 'Taxa de conversão de leads' 
    },
    { 
      id: 6, 
      name: 'Satisfação Cliente', 
      value: '4.7/5.0', 
      trend: 'up', 
      change: '+0.3',
      description: 'NPS médio' 
    }
  ];

  // Buscar dashboards
  const fetchDashboards = async () => {
    setLoading(prev => ({ ...prev, dashboards: true }));
    try {
      const response = await biAPI.getDashboards();
      setDashboards(response || []);
    } catch (error) {
      console.error('Erro ao buscar dashboards:', error);
      setDashboards([]);
    } finally {
      setLoading(prev => ({ ...prev, dashboards: false }));
    }
  };

  // Buscar tendência de KPIs
  const fetchTendencia = async (kpi, periodo) => {
    try {
      const kpiToCalculate = kpiList.find(k => 
        k.nome.toLowerCase().includes(kpi.toLowerCase()) || 
        k.tipo === kpi
      );
      
      if (kpiToCalculate) {
        const response = await biAPI.calculateKPI(kpiToCalculate.id, {
          periodo: periodo,
          agrupamento: 'diario'
        });
        setTendenciaData(response.dados || []);
      } else {
        // Se não encontrar KPI específico, busca análise geral
        const response = await biAPI.getTrendAnalysis({
          metrica: kpi,
          periodo: periodo,
          limite: 10
        });
        setTendenciaData(response || []);
      }
    } catch (error) {
      console.error('Erro ao buscar tendência:', error);
      setTendenciaData([]);
    }
  };

  // Executar relatório predefinido
  const runPredefinedReport = async (reportType) => {
    try {
      let endpoint = '';
      let params = {};
      
      switch(reportType) {
        case 'vendas_vendedor':
          const kpiVendas = kpiList.find(k => k.nome.toLowerCase().includes('venda'));
          if (kpiVendas) {
            const response = await biAPI.calculateKPI(kpiVendas.id, {
              agrupamento: 'vendedor',
              periodo: 'mensal'
            });
            setExportData(response.dados || []);
            alert(`Relatório ${reportType} executado! ${response.dados?.length || 0} registros encontrados.`);
          }
          break;
        case 'vendas_mensais':
          const response = await biAPI.getComparativeAnalysis({
            metrica: 'vendas',
            periodo: 'mensal',
            meses: 12
          });
          setExportData(response || []);
          alert(`Relatório ${reportType} executado! ${response?.length || 0} meses analisados.`);
          break;
        case 'clientes_ativos':
          const performanceResponse = await biAPI.getPerformanceReport({
            tipo: 'clientes',
            top_n: 10
          });
          setExportData(performanceResponse || []);
          alert(`Relatório ${reportType} executado! ${performanceResponse?.length || 0} clientes encontrados.`);
          break;
        case 'tickets_tipo':
          const analysisResponse = await biAPI.getTrendAnalysis({
            metrica: 'tickets',
            agrupamento: 'tipo',
            periodo: 'mensal'
          });
          setExportData(analysisResponse || []);
          alert(`Relatório ${reportType} executado! ${analysisResponse?.length || 0} tipos analisados.`);
          break;
        default:
          return;
      }
    } catch (error) {
      console.error('Erro ao executar relatório:', error);
      alert('Erro ao executar relatório: ' + error.message);
    }
  };

  // Exportar dados
  const exportDataToFormat = async (formato, tipo) => {
    try {
      let dataToExport = exportData;
      
      // Se não houver dados específicos para exportar, busca alguns
      if (!dataToExport || dataToExport.length === 0) {
        const response = await biAPI.getPerformanceReport({
          tipo: tipo,
          limite: 100
        });
        dataToExport = response || [];
      }
      
      if (formato === 'csv') {
        // Criar arquivo CSV para download
        const headers = Object.keys(dataToExport[0] || {}).join(',');
        const rows = dataToExport.map(row => 
          Object.values(row).map(value => 
            typeof value === 'string' ? `"${value.replace(/"/g, '""')}"` : value
          ).join(',')
        );
        const csvContent = [headers, ...rows].join('\n');
        
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${tipo}_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      } else {
        // Para JSON, podemos mostrar em uma nova janela ou baixar
        const jsonStr = JSON.stringify(dataToExport, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${tipo}_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      }
      
      alert(`Dados exportados em ${formato.toUpperCase()}. Total: ${dataToExport.length} registros.`);
    } catch (error) {
      console.error('Erro ao exportar dados:', error);
      alert('Erro ao exportar dados: ' + error.message);
    }
  };

  // Executar query SQL customizada (substituído por análise via API)
  const executeCustomAnalysis = async (analysisType) => {
    try {
      let response;
      
      switch(analysisType) {
        case 'vendedor_performance':
          response = await biAPI.getPerformanceReport({
            tipo: 'vendedor',
            periodo: 'mensal',
            limite: 5
          });
          break;
        case 'clientes_ticket':
          response = await biAPI.getComparativeAnalysis({
            metrica: 'ticket_medio',
            agrupamento: 'cliente'
          });
          break;
        default:
          response = await biAPI.getTrendAnalysis({
            metrica: 'vendas',
            periodo: 'diario',
            dias: 30
          });
      }
      
      setExportData(response || []);
      alert(`Análise executada! ${response?.length || 0} registros retornados.`);
    } catch (error) {
      console.error('Erro ao executar análise:', error);
      alert('Erro ao executar análise: ' + error.message);
    }
  };

  // Buscar dados de dashboard específico
  const fetchDashboardData = async (dashboardId, atualizarCache = false) => {
    try {
      const response = await biAPI.getDashboardData(dashboardId, {
        atualizar_cache: atualizarCache,
        formato: 'json'
      });
      
      setSelectedDashboard(dashboardId);
      setDashboardData(response);
      
      // Se houver dados exportáveis, atualiza a seção de exportação
      if (response && response.dados) {
        setExportData(response.dados.slice(0, 100)); // Limita a 100 registros para visualização
      }
      
      alert(`Dashboard ${dashboardId} carregado! ${response?.dados?.length || 0} registros disponíveis.`);
    } catch (error) {
      console.error('Erro ao buscar dados do dashboard:', error);
      alert('Erro ao carregar dados do dashboard: ' + error.message);
    }
  };

  // Atualizar cache do dashboard
  const refreshDashboardCache = async (dashboardId) => {
    try {
      const response = await biAPI.refreshCache(dashboardId);
      alert(`Cache do dashboard ${dashboardId} atualizado! ${response?.registros || 0} registros atualizados.`);
      
      // Recarrega os dados do dashboard
      if (selectedDashboard === dashboardId) {
        fetchDashboardData(dashboardId, false);
      }
    } catch (error) {
      console.error('Erro ao atualizar cache:', error);
      alert('Erro ao atualizar cache: ' + error.message);
    }
  };

  // Carregar dados iniciais
  useEffect(() => {
    fetchKpis();
    fetchDashboards();
  }, []);

  // Atualizar tendência quando seleção mudar
  useEffect(() => {
    if (selectedKpi && selectedPeriodo) {
      fetchTendencia(selectedKpi, selectedPeriodo);
    }
  }, [selectedKpi, selectedPeriodo, kpiList]);

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
            <div className="header-actions">
              <select 
                value={selectedKpi}
                onChange={(e) => setSelectedKpi(e.target.value)}
                className="form-control-sm"
                style={{ marginRight: '10px' }}
              >
                <option value="">Selecione um KPI</option>
                {kpiList.slice(0, 10).map(kpi => (
                  <option key={kpi.id} value={kpi.tipo || kpi.nome.toLowerCase()}>
                    {kpi.nome}
                  </option>
                ))}
              </select>
              <button 
                onClick={fetchKpis}
                className="btn btn-secondary btn-sm"
                disabled={loading.kpis}
              >
                {loading.kpis ? 'Atualizando...' : '🔄 Atualizar KPIs'}
              </button>
            </div>
          </div>
          
          <div className="kpi-grid">
            {loading.kpis ? (
              <div className="loading">Carregando KPIs...</div>
            ) : (
              kpis.map((kpi, index) => (
                <div key={kpi.id || index} className="kpi-card">
                  <div className="kpi-header">
                    <h3>{kpi.name}</h3>
                    <span className={`trend trend-${kpi.trend}`}>
                      {kpi.change}
                    </span>
                  </div>
                  <div className="kpi-value">{kpi.value}</div>
                  <div className="kpi-trend">
                    {kpi.trend === 'up' ? '📈' : kpi.trend === 'down' ? '📉' : '➡️'} 
                    {kpi.trend === 'up' ? ' Positivo' : kpi.trend === 'down' ? ' Negativo' : ' Estável'}
                  </div>
                  <div className="kpi-description">
                    {kpi.description}
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
                <option value="faturamento">Faturamento</option>
                <option value="custo">Custos</option>
              </select>
              <select 
                value={selectedPeriodo}
                onChange={(e) => setSelectedPeriodo(e.target.value)}
                className="form-control-sm"
              >
                <option value="diario">Diário</option>
                <option value="semanal">Semanal</option>
                <option value="mensal">Mensal</option>
              </select>
              <button 
                onClick={() => fetchTendencia(selectedKpi, selectedPeriodo)}
                className="btn btn-primary btn-sm"
              >
                Atualizar
              </button>
            </div>
          </div>
          
          {tendenciaData.length > 0 ? (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    {Object.keys(tendenciaData[0] || {}).map((key, index) => (
                      <th key={index}>{key.charAt(0).toUpperCase() + key.slice(1)}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {tendenciaData.map((item, index) => (
                    <tr key={index}>
                      {Object.values(item).map((value, colIndex) => (
                        <td key={colIndex}>
                          {typeof value === 'number' 
                            ? key === 'valor' || key === 'total' 
                              ? biAPI.formatCurrency(value)
                              : biAPI.formatNumber(value)
                            : String(value)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p>Nenhum dado de tendência disponível. Selecione um KPI e período.</p>
          )}
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
                    <tr key={dashboard.id || dashboard.id_dashboard}>
                      <td><strong>{dashboard.nome}</strong></td>
                      <td>{dashboard.descricao || 'Sem descrição'}</td>
                      <td>
                        {dashboard.data_atualizacao 
                          ? biAPI.formatDateTime(dashboard.data_atualizacao)
                          : 'N/A'}
                      </td>
                      <td>
                        <div className="action-buttons">
                          <button 
                            onClick={() => fetchDashboardData(dashboard.id || dashboard.id_dashboard, false)}
                            className="btn btn-primary btn-sm"
                          >
                            Ver Dados
                          </button>
                          <button 
                            onClick={() => refreshDashboardCache(dashboard.id || dashboard.id_dashboard)}
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

        {/* Dados do Dashboard Selecionado */}
        {dashboardData && selectedDashboard && (
          <div className="card">
            <div className="section-header">
              <h3>Dados do Dashboard</h3>
              <button 
                onClick={() => {
                  setDashboardData(null);
                  setSelectedDashboard(null);
                }}
                className="btn btn-danger btn-sm"
              >
                Fechar
              </button>
            </div>
            <div className="dashboard-preview">
              <p><strong>Total de Registros:</strong> {dashboardData.dados?.length || 0}</p>
              <p><strong>Última Atualização:</strong> {dashboardData.ultima_atualizacao || 'N/A'}</p>
              
              {dashboardData.dados && dashboardData.dados.length > 0 && (
                <div className="table-container" style={{ maxHeight: '300px', overflowY: 'auto' }}>
                  <table>
                    <thead>
                      <tr>
                        {Object.keys(dashboardData.dados[0]).map((key, index) => (
                          <th key={index}>{key}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {dashboardData.dados.slice(0, 10).map((row, rowIndex) => (
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
                  {dashboardData.dados.length > 10 && (
                    <p className="text-muted">Mostrando 10 de {dashboardData.dados.length} registros</p>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

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
              <p>Vendas totais por mês (últimos 12 meses)</p>
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

        {/* Seção de Análises Customizadas */}
        <div className="card">
          <h2>Análises Customizadas</h2>
          <div className="sql-query-section">
            <div className="form-group">
              <label>Selecione o tipo de análise:</label>
              <select 
                id="analysisType"
                className="form-control"
                defaultValue="vendedor_performance"
              >
                <option value="vendedor_performance">Performance de Vendedores</option>
                <option value="clientes_ticket">Ticket Médio por Cliente</option>
                <option value="vendas_diarias">Vendas Diárias (30 dias)</option>
              </select>
            </div>
            <button 
              onClick={() => {
                const analysisType = document.getElementById('analysisType').value;
                executeCustomAnalysis(analysisType);
              }}
              className="btn btn-primary"
            >
              Executar Análise
            </button>
          </div>
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
                <option value="dashboard">Dashboard Atual</option>
              </select>
              
              <select id="exportFormat" className="form-control">
                <option value="json">JSON</option>
                <option value="csv">CSV</option>
              </select>
              
              <button 
                onClick={() => {
                  const tipo = document.getElementById('exportType').value;
                  const formato = document.getElementById('exportFormat').value;
                  const finalTipo = tipo === 'dashboard' && selectedDashboard ? 'dashboard_' + selectedDashboard : tipo;
                  exportDataToFormat(formato, finalTipo);
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
                onClick={() => exportDataToFormat('json', 'dashboard')}
                className="btn btn-secondary"
                disabled={!selectedDashboard}
              >
                📋 Exportar Dashboard para JSON
              </button>
            </div>
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