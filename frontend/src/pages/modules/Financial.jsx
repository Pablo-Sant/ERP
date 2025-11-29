import React, { useState } from 'react';
import "../../styles/Module.css";

const Financial = () => {
  const [accounts, setAccounts] = useState([
    {
      id: 1,
      type: 'Pagar',
      description: 'Aluguel',
      value: 'R$ 2.500',
      dueDate: '2024-01-05',
      status: 'Pendente'
    },
    {
      id: 2,
      type: 'Receber',
      description: 'Venda Cliente A',
      value: 'R$ 8.750',
      dueDate: '2024-01-10',
      status: 'Recebido'
    },
    {
      id: 3,
      type: 'Pagar',
      description: 'Fornecedor X',
      value: 'R$ 1.200',
      dueDate: '2024-01-08',
      status: 'Pago'
    }
  ]);

  const [newAccount, setNewAccount] = useState({
    type: 'Pagar',
    description: '',
    value: '',
    dueDate: '',
    status: 'Pendente'
  });

  const addAccount = () => {
    if (newAccount.description && newAccount.value) {
      const account = {
        ...newAccount,
        id: Date.now()
      };
      setAccounts([...accounts, account]);
      setNewAccount({
        type: 'Pagar',
        description: '',
        value: '',
        dueDate: '',
        status: 'Pendente'
      });
    }
  };

  const deleteAccount = (id) => {
    setAccounts(accounts.filter(account => account.id !== id));
  };

  const updateStatus = (id, newStatus) => {
    setAccounts(accounts.map(account => 
      account.id === id ? { ...account, status: newStatus } : account
    ));
  };

  const totalReceber = accounts
    .filter(acc => acc.type === 'Receber' && acc.status === 'Pendente')
    .reduce((sum, acc) => sum + parseFloat(acc.value.replace('R$ ', '').replace('.', '').replace(',', '.')), 0);

  const totalPagar = accounts
    .filter(acc => acc.type === 'Pagar' && acc.status === 'Pendente')
    .reduce((sum, acc) => sum + parseFloat(acc.value.replace('R$ ', '').replace('.', '').replace(',', '.')), 0);

  return (
    <div className="module">
      <div className="module-header">
        <h1>Financeiro</h1>
        <p>Contas a pagar/receber e orçamento</p>
      </div>

      <div className="module-content">
        <div className="financial-summary">
          <div className="summary-card receber">
            <h3>A Receber</h3>
            <p className="amount">R$ {totalReceber.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</p>
          </div>
          <div className="summary-card pagar">
            <h3>A Pagar</h3>
            <p className="amount">R$ {totalPagar.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</p>
          </div>
          <div className="summary-card saldo">
            <h3>Saldo</h3>
            <p className="amount">R$ {(totalReceber - totalPagar).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</p>
          </div>
        </div>

        <div className="card">
          <h2>Nova Conta</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Tipo</label>
              <select
                value={newAccount.type}
                onChange={(e) => setNewAccount({...newAccount, type: e.target.value})}
              >
                <option value="Pagar">Conta a Pagar</option>
                <option value="Receber">Conta a Receber</option>
              </select>
            </div>
            <div className="form-group">
              <label>Descrição</label>
              <input
                type="text"
                value={newAccount.description}
                onChange={(e) => setNewAccount({...newAccount, description: e.target.value})}
                placeholder="Descrição da conta"
              />
            </div>
            <div className="form-group">
              <label>Valor</label>
              <input
                type="text"
                value={newAccount.value}
                onChange={(e) => setNewAccount({...newAccount, value: e.target.value})}
                placeholder="R$ 0,00"
              />
            </div>
            <div className="form-group">
              <label>Data Vencimento</label>
              <input
                type="date"
                value={newAccount.dueDate}
                onChange={(e) => setNewAccount({...newAccount, dueDate: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Status</label>
              <select
                value={newAccount.status}
                onChange={(e) => setNewAccount({...newAccount, status: e.target.value})}
              >
                <option value="Pendente">Pendente</option>
                <option value="Pago">Pago</option>
                <option value="Recebido">Recebido</option>
              </select>
            </div>
            <div className="form-group">
              <button onClick={addAccount} className="btn btn-primary">
                Adicionar Conta
              </button>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Contas</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Tipo</th>
                  <th>Descrição</th>
                  <th>Valor</th>
                  <th>Vencimento</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {accounts.map(account => (
                  <tr key={account.id}>
                    <td>
                      <span className={`type-badge type-${account.type.toLowerCase()}`}>
                        {account.type}
                      </span>
                    </td>
                    <td>{account.description}</td>
                    <td><strong>{account.value}</strong></td>
                    <td>{account.dueDate}</td>
                    <td>
                      <select
                        value={account.status}
                        onChange={(e) => updateStatus(account.id, e.target.value)}
                        className={`status-select status-${account.status.toLowerCase()}`}
                      >
                        <option value="Pendente">Pendente</option>
                        <option value="Pago">Pago</option>
                        <option value="Recebido">Recebido</option>
                      </select>
                    </td>
                    <td>
                      <button 
                        onClick={() => deleteAccount(account.id)}
                        className="btn btn-danger btn-sm"
                      >
                        Excluir
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Financial;