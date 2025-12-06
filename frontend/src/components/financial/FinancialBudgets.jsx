// src/components/financial/FinancialBudgets.jsx
import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const FinancialBudgets = ({ onRefresh, loading }) => {
  const [budgets, setBudgets] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    ano: new Date().getFullYear(),
    mes: new Date().getMonth() + 1,
    id_conta: '',
    valor_previsto: '',
    categoria: 'Geral', // Agora existe no banco!
    descricao: '' // Agora existe no banco!
  });
  
  // Novo estado para filtros
  const [filters, setFilters] = useState({
    categoria: '',
    ano: '',
    mes: ''
  });
  
  const [accounts, setAccounts] = useState([]);
  const [loadingBudgets, setLoadingBudgets] = useState(true);
  const [error, setError] = useState(null);
  const [categoriasDisponiveis, setCategoriasDisponiveis] = useState([]);

  // Buscar orçamentos COM os novos campos
  const fetchBudgets = async () => {
    setLoadingBudgets(true);
    setError(null);
    try {
      // Construir query string com filtros
      const queryParams = new URLSearchParams();
      if (filters.categoria) queryParams.append('categoria', filters.categoria);
      if (filters.ano) queryParams.append('ano', filters.ano);
      if (filters.mes) queryParams.append('mes', filters.mes);
      
      const queryString = queryParams.toString();
      const url = `/fi/orcamentos${queryString ? `?${queryString}` : ''}`;
      
      const response = await api.get(url);
      console.log('Dados com categoria e descrição:', response.data);
      
      // Extrair categorias únicas para o filtro
      const categorias = [...new Set(response.data
        .map(item => item.categoria)
        .filter(Boolean)
      )];
      setCategoriasDisponiveis(categorias);
      
      setBudgets(response.data);
    } catch (error) {
      console.error('Erro ao carregar orçamentos:', error);
      setError('Não foi possível carregar os orçamentos do banco de dados.');
      setBudgets([]);
    } finally {
      setLoadingBudgets(false);
    }
  };

  // Buscar contas
  const fetchAccounts = async () => {
    try {
      const response = await api.get('/fi/contas');
      console.log('Contas:', response.data);
      
      setAccounts(response.data);
      if (response.data.length > 0) {
        setFormData(prev => ({
          ...prev,
          id_conta: response.data[0].id_conta
        }));
      }
    } catch (error) {
      console.error('Erro ao carregar contas:', error);
      setAccounts([]);
    }
  };

  // Atualizar registros antigos com os novos campos
  const atualizarCamposAntigos = async () => {
    try {
      const response = await api.post('/fi/orcamentos/atualizar-todos-campos');
      alert(response.data.message);
      fetchBudgets(); // Recarregar dados
    } catch (error) {
      console.error('Erro ao atualizar campos:', error);
      alert('Erro ao atualizar campos: ' + error.message);
    }
  };

  useEffect(() => {
    fetchBudgets();
    fetchAccounts();
  }, []);

  // Criar orçamento COM os novos campos
  const handleAddBudget = async () => {
    if (!formData.valor_previsto || !formData.id_conta) {
      alert('Preencha o valor previsto e selecione uma conta!');
      return;
    }

    try {
      console.log('Enviando dados completos:', formData);
      
      const response = await api.post('/fi/orcamentos', {
        ...formData,
        valor_previsto: parseFloat(formData.valor_previsto)
      });
      
      console.log('Resposta:', response.data);
      
      // Limpar formulário
      setFormData({
        ano: new Date().getFullYear(),
        mes: new Date().getMonth() + 1,
        id_conta: accounts[0]?.id_conta || '',
        valor_previsto: '',
        categoria: 'Geral',
        descricao: ''
      });
      
      setShowForm(false);
      await fetchBudgets();
      
      alert('Orçamento criado com sucesso!');
    } catch (error) {
      console.error('Erro:', error);
      alert(error.response?.data?.detail || 'Erro ao criar orçamento');
    }
  };

  // Aplicar filtros
  const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const aplicarFiltros = () => {
    fetchBudgets();
  };

  const limparFiltros = () => {
    setFilters({
      categoria: '',
      ano: '',
      mes: ''
    });
    fetchBudgets();
  };

  // Calcular totais
  const totalPrevisto = budgets.reduce((sum, b) => sum + (b.valor_previsto || 0), 0);
  const totalRealizado = budgets.reduce((sum, b) => sum + (b.valor_realizado || 0), 0);
  const percentual = totalPrevisto > 0 ? (totalRealizado / totalPrevisto * 100).toFixed(1) : 0;

  // Loading state
  if (loadingBudgets) {
    return (
      <div className="financial-budgets loading">
        <div className="loading-spinner"></div>
        <p>Carregando orçamentos...</p>
      </div>
    );
  }

  return (
    <div className="financial-budgets">
      <div className="budgets-header">
        <h2>Orçamentos</h2>
        
        {error && (
          <div className="error-message">
            ⚠️ {error}
            <button onClick={fetchBudgets} className="btn-retry">Tentar novamente</button>
          </div>
        )}
        
        <div className="budgets-summary">
          <div className="summary-item">
            <span className="label">Total Previsto:</span>
            <span className="value">R$ {totalPrevisto.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
          </div>
          <div className="summary-item">
            <span className="label">Total Realizado:</span>
            <span className="value">R$ {totalRealizado.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
          </div>
          <div className="summary-item">
            <span className="label">Percentual:</span>
            <span className={`value ${percentual <= 100 ? 'positive' : 'negative'}`}>
              {percentual}%
            </span>
          </div>
        </div>
      </div>

      {/* Barra de Filtros */}
      <div className="filters-bar">
        <div className="filter-group">
          <label>Categoria:</label>
          <select 
            value={filters.categoria}
            onChange={(e) => handleFilterChange('categoria', e.target.value)}
          >
            <option value="">Todas as categorias</option>
            {categoriasDisponiveis.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group">
          <label>Ano:</label>
          <input
            type="number"
            value={filters.ano}
            onChange={(e) => handleFilterChange('ano', e.target.value)}
            placeholder="Filtrar por ano"
            min="2020"
            max="2030"
          />
        </div>
        
        <div className="filter-group">
          <label>Mês:</label>
          <select
            value={filters.mes}
            onChange={(e) => handleFilterChange('mes', e.target.value)}
          >
            <option value="">Todos os meses</option>
            {Array.from({length: 12}, (_, i) => (
              <option key={i + 1} value={i + 1}>
                {new Date(2000, i, 1).toLocaleString('pt-BR', { month: 'long' })}
              </option>
            ))}
          </select>
        </div>
        
        <div className="filter-actions">
          <button className="btn btn-secondary" onClick={aplicarFiltros}>
            🔍 Aplicar Filtros
          </button>
          <button className="btn btn-outline" onClick={limparFiltros}>
            🗑️ Limpar
          </button>
        </div>
      </div>

      <div className="budgets-actions">
        <button className="btn btn-primary" onClick={() => setShowForm(true)}>
          + Novo Orçamento
        </button>
        <button className="btn btn-secondary" onClick={fetchBudgets}>
          🔄 Atualizar
        </button>
        <button className="btn btn-info" onClick={atualizarCamposAntigos}>
          🔄 Atualizar Campos Antigos
        </button>
        <button 
          className="btn btn-success" 
          onClick={() => api.post('/fi/orcamentos/inicializar-tabela')
            .then(() => {
              alert('Tabela inicializada!');
              fetchBudgets();
            })
          }
        >
          🚀 Inicializar Tabela
        </button>
      </div>

      {/* Modal de criação */}
      {showForm && (
        <div className="budget-form-modal">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Novo Orçamento</h3>
              <button className="close-btn" onClick={() => setShowForm(false)}>✕</button>
            </div>
            
            <div className="modal-info success">
              <p>✅ Agora os campos <strong>categoria</strong> e <strong>descrição</strong> são salvos no banco de dados!</p>
            </div>
            
            <div className="form-grid">
              <div className="form-group">
                <label>Ano *</label>
                <input
                  type="number"
                  value={formData.ano}
                  onChange={(e) => setFormData({...formData, ano: parseInt(e.target.value)})}
                  min="2020"
                  max="2030"
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Mês *</label>
                <select
                  value={formData.mes}
                  onChange={(e) => setFormData({...formData, mes: parseInt(e.target.value)})}
                  required
                >
                  {Array.from({length: 12}, (_, i) => (
                    <option key={i + 1} value={i + 1}>
                      {new Date(2000, i, 1).toLocaleString('pt-BR', { month: 'long' })}
                    </option>
                  ))}
                </select>
              </div>
              
              <div className="form-group">
                <label>Conta *</label>
                <select
                  value={formData.id_conta}
                  onChange={(e) => setFormData({...formData, id_conta: e.target.value})}
                  required
                >
                  <option value="">Selecione uma conta</option>
                  {accounts.map(account => (
                    <option key={account.id_conta} value={account.id_conta}>
                      {account.nome} (ID: {account.id_conta})
                    </option>
                  ))}
                </select>
              </div>
              
              <div className="form-group">
                <label>Categoria *</label>
                <input
                  type="text"
                  value={formData.categoria}
                  onChange={(e) => setFormData({...formData, categoria: e.target.value})}
                  placeholder="Ex: Marketing, TI, RH..."
                  required
                  list="categorias-sugeridas"
                />
                <datalist id="categorias-sugeridas">
                  {categoriasDisponiveis.map(cat => (
                    <option key={cat} value={cat} />
                  ))}
                  <option value="Marketing" />
                  <option value="TI" />
                  <option value="RH" />
                  <option value="Vendas" />
                  <option value="Compras" />
                  <option value="Manutenção" />
                  <option value="Transporte" />
                </datalist>
              </div>
              
              <div className="form-group">
                <label>Valor Previsto (R$) *</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.valor_previsto}
                  onChange={(e) => setFormData({...formData, valor_previsto: e.target.value})}
                  placeholder="0.00"
                  required
                />
              </div>
              
              <div className="form-group full-width">
                <label>Descrição</label>
                <textarea
                  value={formData.descricao}
                  onChange={(e) => setFormData({...formData, descricao: e.target.value})}
                  placeholder="Descreva este orçamento..."
                  rows="3"
                />
              </div>
            </div>
            
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={() => setShowForm(false)}>
                Cancelar
              </button>
              <button className="btn btn-primary" onClick={handleAddBudget}>
                Salvar no Banco
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Tabela com dados */}
      <div className="budgets-table">
        {budgets.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Ano/Mês</th>
                <th>Categoria</th>
                <th>Descrição</th>
                <th>Previsto</th>
                <th>Realizado</th>
                <th>%</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {budgets.map(budget => {
                const percent = budget.valor_previsto > 0 
                  ? ((budget.valor_realizado || 0) / budget.valor_previsto * 100).toFixed(1)
                  : 0;
                  
                const categoriaCor = {
                  'Marketing': '#4CAF50',
                  'TI': '#2196F3',
                  'RH': '#FF9800',
                  'Vendas': '#E91E63',
                  'Compras': '#9C27B0',
                  'Manutenção': '#795548',
                  'Transporte': '#607D8B'
                }[budget.categoria] || '#9E9E9E';
                
                return (
                  <tr key={budget.id_orcamento}>
                    <td>
                      <strong>{budget.ano}/{budget.mes.toString().padStart(2, '0')}</strong>
                    </td>
                    <td>
                      <span 
                        className="category-badge"
                        style={{
                          backgroundColor: categoriaCor + '20',
                          color: categoriaCor,
                          borderColor: categoriaCor
                        }}
                      >
                        {budget.categoria || 'Sem categoria'}
                      </span>
                    </td>
                    <td className="description-cell">
                      {budget.descricao || 'Sem descrição'}
                    </td>
                    <td>
                      <span className="amount">
                        R$ {budget.valor_previsto?.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                      </span>
                    </td>
                    <td>
                      <span className="amount">
                        R$ {(budget.valor_realizado || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                      </span>
                    </td>
                    <td>
                      <span className={`percent ${percent <= 100 ? 'positive' : 'negative'}`}>
                        {percent}%
                      </span>
                    </td>
                    <td>
                      <span className={`status-badge ${percent <= 100 ? 'success' : 'warning'}`}>
                        {percent <= 100 ? '✅ Dentro' : '⚠️ Acima'}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <div className="empty-icon">📋</div>
            <h3>Nenhum orçamento encontrado</h3>
            <p>Clique em "Novo Orçamento" para começar.</p>
            <button 
              className="btn btn-success" 
              onClick={() => api.post('/fi/orcamentos/inicializar-tabela')
                .then(() => {
                  alert('Dados de exemplo criados!');
                  fetchBudgets();
                })
              }
            >
              🚀 Criar Dados de Exemplo
            </button>
          </div>
        )}
      </div>

      {/* Estatísticas */}
      <div className="stats-summary">
        <div className="stat-item">
          <h4>Resumo por Categoria</h4>
          {(() => {
            const porCategoria = budgets.reduce((acc, budget) => {
              const cat = budget.categoria || 'Não categorizado';
              if (!acc[cat]) acc[cat] = { previsto: 0, realizado: 0 };
              acc[cat].previsto += budget.valor_previsto || 0;
              acc[cat].realizado += budget.valor_realizado || 0;
              return acc;
            }, {});
            
            return Object.entries(porCategoria).map(([cat, valores]) => {
              const percent = valores.previsto > 0 ? (valores.realizado / valores.previsto * 100).toFixed(1) : 0;
              return (
                <div key={cat} className="category-stat">
                  <span className="cat-name">{cat}</span>
                  <span className="cat-values">
                    R$ {valores.realizado.toLocaleString('pt-BR')} / R$ {valores.previsto.toLocaleString('pt-BR')}
                  </span>
                  <span className={`cat-percent ${percent <= 100 ? 'positive' : 'negative'}`}>
                    {percent}%
                  </span>
                </div>
              );
            });
          })()}
        </div>
      </div>
    </div>
  );
};

export default FinancialBudgets;