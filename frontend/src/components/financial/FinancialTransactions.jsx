// src/components/financial/FinancialTransactions.jsx
import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const FinancialTransactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    type: 'all',
    account_id: 'all',
    start_date: '',
    end_date: ''
  });
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    id_conta: '',
    descricao: '',
    tipo: 'receita',
    valor: '',
    data_lancamento: new Date().toISOString().split('T')[0],
    categoria: '',
    observacoes: ''
  });

  // Buscar transações
  const fetchTransactions = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filters.type !== 'all') params.tipo = filters.type;
      if (filters.account_id !== 'all') params.conta_id = filters.account_id;
      if (filters.start_date) params.data_inicio = filters.start_date;
      if (filters.end_date) params.data_fim = filters.end_date;

      const response = await api.get('/fi/lancamentos', { params });
      setTransactions(response.data);
    } catch (error) {
      console.error('Erro ao carregar transações:', error);
    } finally {
      setLoading(false);
    }
  };

  // Buscar contas para o select
  const fetchAccounts = async () => {
    try {
      const response = await api.get('/fi/contas');
      setAccounts(response.data);
    } catch (error) {
      console.error('Erro ao carregar contas:', error);
    }
  };

  // Carregar dados iniciais
  useEffect(() => {
    fetchTransactions();
    fetchAccounts();
  }, []);

  // Aplicar filtros
  const applyFilters = () => {
    fetchTransactions();
  };

  // Limpar filtros
  const clearFilters = () => {
    setFilters({
      type: 'all',
      account_id: 'all',
      start_date: '',
      end_date: ''
    });
    fetchTransactions();
  };

  // Criar nova transação
  const handleCreateTransaction = async () => {
    try {
      await api.post('/fi/lancamentos', {
        ...formData,
        valor: parseFloat(formData.valor)
      });
      
      // Limpar formulário
      setFormData({
        id_conta: '',
        descricao: '',
        tipo: 'receita',
        valor: '',
        data_lancamento: new Date().toISOString().split('T')[0],
        categoria: '',
        observacoes: ''
      });
      setShowForm(false);
      fetchTransactions();
      
      alert('Transação criada com sucesso!');
    } catch (error) {
      console.error('Erro ao criar transação:', error);
      alert('Erro ao criar transação: ' + (error.response?.data?.detail || error.message));
    }
  };

  // Calcular totais
  const calculateTotals = () => {
    const income = transactions
      .filter(t => t.tipo === 'receita')
      .reduce((sum, t) => sum + (t.valor || 0), 0);
    
    const expense = transactions
      .filter(t => t.tipo === 'despesa')
      .reduce((sum, t) => sum + (t.valor || 0), 0);
    
    return { income, expense, balance: income - expense };
  };

  const totals = calculateTotals();

  return (
    <div className="financial-transactions">
      <h2>Transações Financeiras</h2>

      {/* Filtros */}
      <div className="filters-card">
        <h3>Filtros</h3>
        <div className="filters-grid">
          <div className="form-group">
            <label>Tipo</label>
            <select
              value={filters.type}
              onChange={(e) => setFilters({...filters, type: e.target.value})}
            >
              <option value="all">Todos</option>
              <option value="receita">Receitas</option>
              <option value="despesa">Despesas</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Conta</label>
            <select
              value={filters.account_id}
              onChange={(e) => setFilters({...filters, account_id: e.target.value})}
            >
              <option value="all">Todas as contas</option>
              {accounts.map(account => (
                <option key={account.id_conta} value={account.id_conta}>
                  {account.nome}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>Data Início</label>
            <input
              type="date"
              value={filters.start_date}
              onChange={(e) => setFilters({...filters, start_date: e.target.value})}
            />
          </div>
          
          <div className="form-group">
            <label>Data Fim</label>
            <input
              type="date"
              value={filters.end_date}
              onChange={(e) => setFilters({...filters, end_date: e.target.value})}
            />
          </div>
        </div>
        
        <div className="filter-actions">
          <button className="btn btn-secondary" onClick={clearFilters}>
            Limpar Filtros
          </button>
          <button className="btn btn-primary" onClick={applyFilters}>
            Aplicar Filtros
          </button>
        </div>
      </div>

      {/* Resumo */}
      <div className="summary-cards">
        <div className="summary-card total-income">
          <h4>Total Receitas</h4>
          <p className="amount">
            R$ {totals.income.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
          </p>
        </div>
        
        <div className="summary-card total-expense">
          <h4>Total Despesas</h4>
          <p className="amount">
            R$ {totals.expense.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
          </p>
        </div>
        
        <div className="summary-card total-balance">
          <h4>Saldo</h4>
          <p className={`amount ${totals.balance >= 0 ? 'positive' : 'negative'}`}>
            R$ {totals.balance.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
          </p>
        </div>
      </div>

      {/* Botão para nova transação */}
      <div className="actions-bar">
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(true)}
        >
          + Nova Transação
        </button>
      </div>

      {/* Formulário de nova transação (modal) */}
      {showForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Nova Transação</h3>
              <button className="close-btn" onClick={() => setShowForm(false)}>✕</button>
            </div>
            
            <div className="form-grid">
              <div className="form-group">
                <label>Tipo *</label>
                <select
                  value={formData.tipo}
                  onChange={(e) => setFormData({...formData, tipo: e.target.value})}
                >
                  <option value="receita">Receita</option>
                  <option value="despesa">Despesa</option>
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
                      {account.nome}
                    </option>
                  ))}
                </select>
              </div>
              
              <div className="form-group">
                <label>Descrição *</label>
                <input
                  type="text"
                  value={formData.descricao}
                  onChange={(e) => setFormData({...formData, descricao: e.target.value})}
                  placeholder="Descrição da transação"
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Valor (R$) *</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.valor}
                  onChange={(e) => setFormData({...formData, valor: e.target.value})}
                  placeholder="0.00"
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Data</label>
                <input
                  type="date"
                  value={formData.data_lancamento}
                  onChange={(e) => setFormData({...formData, data_lancamento: e.target.value})}
                />
              </div>
              
              <div className="form-group">
                <label>Categoria</label>
                <input
                  type="text"
                  value={formData.categoria}
                  onChange={(e) => setFormData({...formData, categoria: e.target.value})}
                  placeholder="Categoria (opcional)"
                />
              </div>
              
              <div className="form-group full-width">
                <label>Observações</label>
                <textarea
                  value={formData.observacoes}
                  onChange={(e) => setFormData({...formData, observacoes: e.target.value})}
                  placeholder="Observações adicionais..."
                  rows="3"
                />
              </div>
            </div>
            
            <div className="modal-actions">
              <button
                className="btn btn-secondary"
                onClick={() => setShowForm(false)}
              >
                Cancelar
              </button>
              <button
                className="btn btn-primary"
                onClick={handleCreateTransaction}
                disabled={!formData.id_conta || !formData.descricao || !formData.valor}
              >
                Salvar Transação
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Lista de transações */}
      <div className="transactions-table">
        <table>
          <thead>
            <tr>
              <th>Data</th>
              <th>Descrição</th>
              <th>Conta</th>
              <th>Tipo</th>
              <th>Valor</th>
              <th>Categoria</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="6" className="loading-row">Carregando transações...</td>
              </tr>
            ) : transactions.length === 0 ? (
              <tr>
                <td colSpan="6" className="empty-row">
                  Nenhuma transação encontrada
                </td>
              </tr>
            ) : (
              transactions.map(transaction => (
                <tr key={transaction.id_lancamento}>
                  <td>
                    {new Date(transaction.data_lancamento).toLocaleDateString('pt-BR')}
                  </td>
                  <td>
                    <div className="transaction-description">
                      {transaction.descricao}
                      {transaction.observacoes && (
                        <span className="transaction-notes">
                          {transaction.observacoes}
                        </span>
                      )}
                    </div>
                  </td>
                  <td>
                    {accounts.find(a => a.id_conta === transaction.id_conta)?.nome || 'N/A'}
                  </td>
                  <td>
                    <span className={`type-badge type-${transaction.tipo}`}>
                      {transaction.tipo === 'receita' ? 'Receita' : 'Despesa'}
                    </span>
                  </td>
                  <td>
                    <span className={`amount ${transaction.tipo}`}>
                      R$ {transaction.valor?.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </span>
                  </td>
                  <td>
                    {transaction.categoria || '-'}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FinancialTransactions;