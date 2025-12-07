// src/components/financial/FinancialAccounts.jsx
import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const FinancialAccounts = () => {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingAccount, setEditingAccount] = useState(null);

  const [formData, setFormData] = useState({
    nome: '',
    tipo: 'corrente',
    banco: '',
    agencia: '',
    conta: '',
    saldo_inicial: '0.00',
    ativo: true
  });

  // Buscar contas
  const fetchAccounts = async () => {
    try {
      setLoading(true);
      const response = await api.get('/fi/contas');
      setAccounts(response.data);
    } catch (error) {
      console.error('Erro ao carregar contas:', error);
    } finally {
      setLoading(false);
    }
  };

  // Carregar contas na inicialização
  useEffect(() => {
    fetchAccounts();
  }, []);

  // Lidar com mudanças no formulário
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  // Criar nova conta
  const handleCreateAccount = async () => {
    try {
      await api.post('/fi/contas', {
        ...formData,
        saldo_inicial: parseFloat(formData.saldo_inicial)
      });
      
      // Limpar formulário e recarregar contas
      setFormData({
        nome: '',
        tipo: 'corrente',
        banco: '',
        agencia: '',
        conta: '',
        saldo_inicial: '0.00',
        ativo: true
      });
      setShowForm(false);
      fetchAccounts();
      
      alert('Conta criada com sucesso!');
    } catch (error) {
      console.error('Erro ao criar conta:', error);
      alert('Erro ao criar conta: ' + (error.response?.data?.detail || error.message));
    }
  };

  // Editar conta
  const handleEditAccount = (account) => {
    setEditingAccount(account);
    setFormData({
      nome: account.nome,
      tipo: account.tipo,
      banco: account.banco || '',
      agencia: account.agencia || '',
      conta: account.conta || '',
      saldo_inicial: account.saldo_inicial || '0.00',
      ativo: account.ativo
    });
    setShowForm(true);
  };

  // Atualizar conta
  const handleUpdateAccount = async () => {
    try {
      await api.put(`/fi/contas/${editingAccount.id_conta}`, formData);
      setEditingAccount(null);
      setShowForm(false);
      fetchAccounts();
      alert('Conta atualizada com sucesso!');
    } catch (error) {
      console.error('Erro ao atualizar conta:', error);
      alert('Erro ao atualizar conta: ' + (error.response?.data?.detail || error.message));
    }
  };

  // Excluir conta
  const handleDeleteAccount = async (accountId) => {
    if (window.confirm('Tem certeza que deseja excluir esta conta?')) {
      try {
        await api.delete(`/fi/contas/${accountId}`);
        fetchAccounts();
        alert('Conta excluída com sucesso!');
      } catch (error) {
        console.error('Erro ao excluir conta:', error);
        alert('Erro ao excluir conta: ' + (error.response?.data?.detail || error.message));
      }
    }
  };

  // Calcular saldo total
  const calculateTotalBalance = () => {
    return accounts.reduce((total, account) => {
      return total + (account.saldo_inicial || 0);
    }, 0);
  };

  return (
    <div className="financial-accounts">
      {/* Cabeçalho com estatísticas */}
      <div className="accounts-header">
        <h2>Contas Financeiras</h2>
        <div className="accounts-stats">
          <div className="stat-item">
            <span className="stat-label">Total de Contas</span>
            <span className="stat-value">{accounts.length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Saldo Total</span>
            <span className="stat-value">
              R$ {calculateTotalBalance().toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
            </span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Contas Ativas</span>
            <span className="stat-value">
              {accounts.filter(a => a.ativo).length}
            </span>
          </div>
        </div>
      </div>

      {/* Botão para adicionar nova conta */}
      <div className="accounts-actions">
        <button
          className="btn btn-primary"
          onClick={() => {
            setEditingAccount(null);
            setShowForm(true);
          }}
        >
          + Nova Conta
        </button>
        
        <button
          className="btn btn-secondary"
          onClick={fetchAccounts}
          disabled={loading}
        >
          {loading ? 'Atualizando...' : 'Atualizar'}
        </button>
      </div>

      {/* Formulário de conta (modal ou inline) */}
      {showForm && (
        <div className="account-form-modal">
          <div className="modal-content">
            <div className="modal-header">
              <h3>{editingAccount ? 'Editar Conta' : 'Nova Conta'}</h3>
              <button className="close-btn" onClick={() => {
                setShowForm(false);
                setEditingAccount(null);
              }}>✕</button>
            </div>
            
            <div className="form-grid">
              <div className="form-group">
                <label>Nome da Conta *</label>
                <input
                  type="text"
                  name="nome"
                  value={formData.nome}
                  onChange={handleInputChange}
                  placeholder="Ex: Conta Corrente Itaú"
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Tipo de Conta</label>
                <select
                  name="tipo"
                  value={formData.tipo}
                  onChange={handleInputChange}
                >
                  <option value="corrente">Conta Corrente</option>
                  <option value="poupanca">Conta Poupança</option>
                  <option value="investimento">Conta Investimento</option>
                  <option value="caixa">Caixa</option>
                  <option value="outros">Outros</option>
                </select>
              </div>
              
              <div className="form-group">
                <label>Banco</label>
                <input
                  type="text"
                  name="banco"
                  value={formData.banco}
                  onChange={handleInputChange}
                  placeholder="Nome do banco"
                />
              </div>
              
              <div className="form-group">
                <label>Agência</label>
                <input
                  type="text"
                  name="agencia"
                  value={formData.agencia}
                  onChange={handleInputChange}
                  placeholder="Número da agência"
                />
              </div>
              
              <div className="form-group">
                <label>Conta</label>
                <input
                  type="text"
                  name="conta"
                  value={formData.conta}
                  onChange={handleInputChange}
                  placeholder="Número da conta"
                />
              </div>
              
              <div className="form-group">
                <label>Saldo Inicial (R$)</label>
                <input
                  type="number"
                  step="0.01"
                  name="saldo_inicial"
                  value={formData.saldo_inicial}
                  onChange={handleInputChange}
                  placeholder="0.00"
                />
              </div>
              
              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="ativo"
                    checked={formData.ativo}
                    onChange={handleInputChange}
                  />
                  <span>Conta ativa</span>
                </label>
              </div>
            </div>
            
            <div className="modal-actions">
              <button
                className="btn btn-secondary"
                onClick={() => {
                  setShowForm(false);
                  setEditingAccount(null);
                }}
              >
                Cancelar
              </button>
              <button
                className="btn btn-primary"
                onClick={editingAccount ? handleUpdateAccount : handleCreateAccount}
              >
                {editingAccount ? 'Atualizar' : 'Criar'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Lista de contas */}
      <div className="accounts-list">
        {loading ? (
          <div className="loading-state">Carregando contas...</div>
        ) : accounts.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🏦</div>
            <h3>Nenhuma conta encontrada</h3>
            <p>Clique em "Nova Conta" para adicionar sua primeira conta financeira.</p>
          </div>
        ) : (
          <div className="accounts-grid">
            {accounts.map(account => (
              <div key={account.id_conta} className="account-card">
                <div className="account-header">
                  <div className="account-info">
                    <h4>{account.nome}</h4>
                    <span className={`account-type ${account.tipo}`}>
                      {account.tipo === 'corrente' ? 'Conta Corrente' : 
                       account.tipo === 'poupanca' ? 'Conta Poupança' :
                       account.tipo === 'investimento' ? 'Investimento' :
                       account.tipo === 'caixa' ? 'Caixa' : 'Outros'}
                    </span>
                  </div>
                  <div className="account-status">
                    <span className={`status-badge ${account.ativo ? 'active' : 'inactive'}`}>
                      {account.ativo ? 'Ativa' : 'Inativa'}
                    </span>
                  </div>
                </div>
                
                <div className="account-details">
                  {account.banco && (
                    <div className="detail-row">
                      <span className="detail-label">Banco:</span>
                      <span className="detail-value">{account.banco}</span>
                    </div>
                  )}
                  {account.agencia && (
                    <div className="detail-row">
                      <span className="detail-label">Agência:</span>
                      <span className="detail-value">{account.agencia}</span>
                    </div>
                  )}
                  {account.conta && (
                    <div className="detail-row">
                      <span className="detail-label">Conta:</span>
                      <span className="detail-value">{account.conta}</span>
                    </div>
                  )}
                  <div className="detail-row">
                    <span className="detail-label">Saldo:</span>
                    <span className="detail-value balance">
                      R$ {account.saldo_inicial?.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) || '0,00'}
                    </span>
                  </div>
                </div>
                
                <div className="account-actions">
                  <button
                    className="btn btn-sm btn-secondary"
                    onClick={() => handleEditAccount(account)}
                  >
                    Editar
                  </button>
                  <button
                    className="btn btn-sm btn-danger"
                    onClick={() => handleDeleteAccount(account.id_conta)}
                  >
                    Excluir
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

const fetchAccounts = async () => {
  try {
    console.log('Tentando buscar contas...');
    
    // Teste 1: Rota sem autenticação
    const testResponse = await axios.get('http://localhost:8000/api/fi/health');
    console.log('Health check:', testResponse.data);
    
    // Teste 2: Rota CORS
    const corsTest = await axios.get('http://localhost:8000/api/fi/cors-test');
    console.log('CORS test:', corsTest.data);
    
    // Teste 3: Tente a rota real
    const response = await axios.get('http://localhost:8000/api/fi/contas', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    
    console.log('Contas recebidas:', response.data);
    setAccounts(response.data);
    
  } catch (error) {
    console.error('ERRO COMPLETO:', error);
    console.error('Status:', error.response?.status);
    console.error('Data:', error.response?.data);
    console.error('Headers:', error.response?.headers);
    
    // Se for erro 401 (não autenticado), redirecione para login
    if (error.response?.status === 401) {
      console.log('Não autenticado. Redirecionando para login...');
      // Redirecionar para página de login
    }
  }
};

export default FinancialAccounts;