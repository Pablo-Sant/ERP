// src/components/financial/FinancialReports.jsx
import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const FinancialReports = ({ onRefresh, loading }) => {
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState('receitas_despesas');
  const [dateRange, setDateRange] = useState({
    start: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
    end: new Date().toISOString().split('T')[0]
  });
  const [reportData, setReportData] = useState(null);
  const [generating, setGenerating] = useState(false);

  const reportTypes = [
    { id: 'receitas_despesas', name: 'Receitas x Despesas', icon: '📊' },
    { id: 'fluxo_caixa', name: 'Fluxo de Caixa', icon: '💰' },
    { id: 'balanco', name: 'Balanço', icon: '⚖️' },
    { id: 'categorias', name: 'Por Categoria', icon: '🏷️' }
  ];

  // Gerar relatório
  const generateReport = async () => {
    try {
      setGenerating(true);
      
      let data;
      switch (selectedReport) {
        case 'receitas_despesas':
          data = await api.get('/fi/relatorios/receitas-despesas', {
            params: {
              data_inicio: dateRange.start,
              data_fim: dateRange.end
            }
          });
          setReportData(data.data);
          break;
          
        case 'fluxo_caixa':
          // Simular dados de fluxo de caixa
          setReportData({
            periodo: { inicio: dateRange.start, fim: dateRange.end },
            fluxo: Array.from({length: 30}, (_, i) => ({
              data: new Date(new Date(dateRange.start).getTime() + i * 86400000).toISOString().split('T')[0],
              entradas: Math.random() * 5000,
              saidas: Math.random() * 3000
            }))
          });
          break;
          
        default:
          // Dados simulados
          setReportData({
            periodo: { inicio: dateRange.start, fim: dateRange.end },
            resumo: {
              receitas: 15000,
              despesas: 8000,
              saldo: 7000
            },
            detalhes: [
              { categoria: 'Vendas', valor: 8000, tipo: 'receita' },
              { categoria: 'Serviços', valor: 7000, tipo: 'receita' },
              { categoria: 'Fornecedores', valor: 4000, tipo: 'despesa' },
              { categoria: 'Salários', valor: 3000, tipo: 'despesa' },
              { categoria: 'Impostos', valor: 1000, tipo: 'despesa' }
            ]
          });
      }
      
    } catch (error) {
      console.error('Erro ao gerar relatório:', error);
      alert('Erro ao gerar relatório');
    } finally {
      setGenerating(false);
    }
  };

  // Exportar relatório
  const exportReport = (format) => {
    if (!reportData) {
      alert('Gere um relatório primeiro');
      return;
    }
    
    const dataStr = JSON.stringify(reportData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `relatorio_financeiro_${selectedReport}_${dateRange.start}_${dateRange.end}.${format}`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
    
    alert(`Relatório exportado como ${exportFileDefaultName}`);
  };

  useEffect(() => {
    // Carregar relatórios salvos
    const savedReports = JSON.parse(localStorage.getItem('financial_reports') || '[]');
    setReports(savedReports);
  }, []);

  const renderReportContent = () => {
    if (!reportData) {
      return (
        <div className="report-empty">
          <p>Selecione um tipo de relatório e período, então clique em "Gerar Relatório"</p>
        </div>
      );
    }

    switch (selectedReport) {
      case 'receitas_despesas':
        return (
          <div className="report-content">
            <div className="report-summary">
              <div className="summary-card">
                <h4>Receitas</h4>
                <p className="amount positive">
                  R$ {reportData.resumo?.total_receitas?.toLocaleString('pt-BR') || '0,00'}
                </p>
              </div>
              <div className="summary-card">
                <h4>Despesas</h4>
                <p className="amount negative">
                  R$ {reportData.resumo?.total_despesas?.toLocaleString('pt-BR') || '0,00'}
                </p>
              </div>
              <div className="summary-card">
                <h4>Saldo</h4>
                <p className={`amount ${(reportData.resumo?.saldo_periodo || 0) >= 0 ? 'positive' : 'negative'}`}>
                  R$ {(reportData.resumo?.saldo_periodo || 0).toLocaleString('pt-BR')}
                </p>
              </div>
            </div>
            
            <div className="report-table">
              <h4>Detalhamento</h4>
              <table>
                <thead>
                  <tr>
                    <th>Data</th>
                    <th>Descrição</th>
                    <th>Tipo</th>
                    <th>Valor</th>
                  </tr>
                </thead>
                <tbody>
                  {reportData.lancamentos?.slice(0, 10).map(item => (
                    <tr key={item.id}>
                      <td>{item.data}</td>
                      <td>{item.descricao}</td>
                      <td>
                        <span className={`type-badge type-${item.tipo}`}>
                          {item.tipo === 'receita' ? 'Receita' : 'Despesa'}
                        </span>
                      </td>
                      <td>
                        <span className={`amount ${item.tipo}`}>
                          R$ {item.valor?.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        );

      default:
        return (
          <div className="report-content">
            <div className="report-info">
              <p><strong>Período:</strong> {dateRange.start} a {dateRange.end}</p>
              <p><strong>Tipo:</strong> {reportTypes.find(r => r.id === selectedReport)?.name}</p>
            </div>
            <pre className="report-json">
              {JSON.stringify(reportData, null, 2)}
            </pre>
          </div>
        );
    }
  };

  return (
    <div className="financial-reports">
      <div className="reports-header">
        <h2>Relatórios Financeiros</h2>
        <p>Gere relatórios personalizados para análise das finanças</p>
      </div>

      <div className="reports-controls">
        <div className="controls-grid">
          <div className="form-group">
            <label>Tipo de Relatório</label>
            <select
              value={selectedReport}
              onChange={(e) => setSelectedReport(e.target.value)}
            >
              {reportTypes.map(type => (
                <option key={type.id} value={type.id}>
                  {type.icon} {type.name}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>Data Início</label>
            <input
              type="date"
              value={dateRange.start}
              onChange={(e) => setDateRange({...dateRange, start: e.target.value})}
            />
          </div>
          
          <div className="form-group">
            <label>Data Fim</label>
            <input
              type="date"
              value={dateRange.end}
              onChange={(e) => setDateRange({...dateRange, end: e.target.value})}
            />
          </div>
          
          <div className="form-group">
            <label>Ações</label>
            <div className="action-buttons">
              <button 
                className="btn btn-primary"
                onClick={generateReport}
                disabled={generating}
              >
                {generating ? 'Gerando...' : '📊 Gerar Relatório'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Exportar opções */}
      {reportData && (
        <div className="export-options">
          <h4>Exportar Relatório</h4>
          <div className="export-buttons">
            <button className="btn btn-secondary" onClick={() => exportReport('json')}>
              📥 JSON
            </button>
            <button className="btn btn-secondary" onClick={() => exportReport('txt')}>
              📝 TXT
            </button>
            <button className="btn btn-secondary" onClick={() => window.print()}>
              🖨️ Imprimir
            </button>
          </div>
        </div>
      )}

      {/* Conteúdo do relatório */}
      <div className="report-container">
        {renderReportContent()}
      </div>

      {/* Relatórios salvos */}
      <div className="saved-reports">
        <h3>Relatórios Salvos</h3>
        {reports.length === 0 ? (
          <div className="empty-state">
            <p>Nenhum relatório salvo ainda</p>
          </div>
        ) : (
          <div className="reports-list">
            {reports.slice(0, 5).map((report, index) => (
              <div key={index} className="report-item">
                <div className="report-info">
                  <span className="report-name">{report.name}</span>
                  <span className="report-date">{report.date}</span>
                </div>
                <button className="btn btn-sm">
                  Visualizar
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default FinancialReports;