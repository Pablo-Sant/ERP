import React, { useState } from 'react';
import "../../styles/Module.css";

const Sales = () => {
  const [sales, setSales] = useState([
    {
      id: 1,
      client: 'Empresa ABC Ltda',
      product: 'Sistema ERP Completo',
      value: 'R$ 45.000',
      date: '2024-01-05',
      status: 'Fechada',
      seller: 'Carlos Mendes'
    },
    {
      id: 2,
      client: 'Comércio XYZ',
      product: 'Módulo Vendas',
      value: 'R$ 12.500',
      date: '2024-01-08',
      status: 'Negociação',
      seller: 'Ana Costa'
    },
    {
      id: 3,
      client: 'Indústria 123',
      product: 'Consultoria Implementação',
      value: 'R$ 28.000',
      date: '2024-01-10',
      status: 'Proposta',
      seller: 'Carlos Mendes'
    }
  ]);

  const [clients, setClients] = useState([
    {
      id: 1,
      name: 'Empresa ABC Ltda',
      contact: 'João Silva',
      email: 'joao@empresaabc.com',
      phone: '(11) 3333-3333',
      status: 'Ativo'
    },
    {
      id: 2,
      name: 'Comércio XYZ',
      contact: 'Maria Santos',
      email: 'maria@comercioxyz.com',
      phone: '(11) 4444-4444',
      status: 'Ativo'
    }
  ]);

  const [newSale, setNewSale] = useState({
    client: '',
    product: '',
    value: '',
    date: '',
    status: 'Proposta',
    seller: ''
  });

  const [newClient, setNewClient] = useState({
    name: '',
    contact: '',
    email: '',
    phone: '',
    status: 'Ativo'
  });

  const addSale = () => {
    if (newSale.client && newSale.product) {
      const sale = {
        ...newSale,
        id: Date.now()
      };
      setSales([...sales, sale]);
      setNewSale({
        client: '',
        product: '',
        value: '',
        date: '',
        status: 'Proposta',
        seller: ''
      });
    }
  };

  const addClient = () => {
    if (newClient.name && newClient.contact) {
      const client = {
        ...newClient,
        id: Date.now()
      };
      setClients([...clients, client]);
      setNewClient({
        name: '',
        contact: '',
        email: '',
        phone: '',
        status: 'Ativo'
      });
    }
  };

  const deleteSale = (id) => {
    setSales(sales.filter(sale => sale.id !== id));
  };

  const deleteClient = (id) => {
    setClients(clients.filter(client => client.id !== id));
  };

  const totalSales = sales
    .filter(sale => sale.status === 'Fechada')
    .reduce((sum, sale) => sum + parseFloat(sale.value.replace('R$ ', '').replace('.', '').replace(',', '.')), 0);

  return (
    <div className="module">
      <div className="module-header">
        <h1>Vendas</h1>
        <p>Gestão comercial e CRM</p>
      </div>

      <div className="module-content">
        <div className="sales-summary">
          <div className="summary-card">
            <h3>Vendas do Mês</h3>
            <p className="amount">R$ {totalSales.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</p>
          </div>
          <div className="summary-card">
            <h3>Total de Clientes</h3>
            <p className="count">{clients.length}</p>
          </div>
          <div className="summary-card">
            <h3>Oportunidades</h3>
            <p className="opportunities">{sales.filter(s => s.status !== 'Fechada').length}</p>
          </div>
        </div>

        <div className="card">
          <h2>Nova Venda/Oportunidade</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Cliente</label>
              <select
                value={newSale.client}
                onChange={(e) => setNewSale({...newSale, client: e.target.value})}
              >
                <option value="">Selecione um cliente</option>
                {clients.map(client => (
                  <option key={client.id} value={client.name}>{client.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Produto/Serviço</label>
              <input
                type="text"
                value={newSale.product}
                onChange={(e) => setNewSale({...newSale, product: e.target.value})}
                placeholder="Descrição do produto/serviço"
              />
            </div>
            <div className="form-group">
              <label>Valor</label>
              <input
                type="text"
                value={newSale.value}
                onChange={(e) => setNewSale({...newSale, value: e.target.value})}
                placeholder="R$ 0,00"
              />
            </div>
            <div className="form-group">
              <label>Data</label>
              <input
                type="date"
                value={newSale.date}
                onChange={(e) => setNewSale({...newSale, date: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Status</label>
              <select
                value={newSale.status}
                onChange={(e) => setNewSale({...newSale, status: e.target.value})}
              >
                <option value="Proposta">Proposta</option>
                <option value="Negociação">Negociação</option>
                <option value="Fechada">Fechada</option>
                <option value="Perdida">Perdida</option>
              </select>
            </div>
            <div className="form-group">
              <label>Vendedor</label>
              <input
                type="text"
                value={newSale.seller}
                onChange={(e) => setNewSale({...newSale, seller: e.target.value})}
                placeholder="Nome do vendedor"
              />
            </div>
            <div className="form-group">
              <button onClick={addSale} className="btn btn-primary">
                Adicionar Venda
              </button>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Pipeline de Vendas</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Cliente</th>
                  <th>Produto/Serviço</th>
                  <th>Valor</th>
                  <th>Data</th>
                  <th>Status</th>
                  <th>Vendedor</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {sales.map(sale => (
                  <tr key={sale.id}>
                    <td><strong>{sale.client}</strong></td>
                    <td>{sale.product}</td>
                    <td>{sale.value}</td>
                    <td>{sale.date}</td>
                    <td>
                      <span className={`status-badge status-${sale.status.toLowerCase()}`}>
                        {sale.status}
                      </span>
                    </td>
                    <td>{sale.seller}</td>
                    <td>
                      <button 
                        onClick={() => deleteSale(sale.id)}
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

        <div className="card">
          <h2>Cadastro de Clientes</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Nome da Empresa</label>
              <input
                type="text"
                value={newClient.name}
                onChange={(e) => setNewClient({...newClient, name: e.target.value})}
                placeholder="Razão social"
              />
            </div>
            <div className="form-group">
              <label>Contato</label>
              <input
                type="text"
                value={newClient.contact}
                onChange={(e) => setNewClient({...newClient, contact: e.target.value})}
                placeholder="Nome do contato"
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={newClient.email}
                onChange={(e) => setNewClient({...newClient, email: e.target.value})}
                placeholder="email@empresa.com"
              />
            </div>
            <div className="form-group">
              <label>Telefone</label>
              <input
                type="text"
                value={newClient.phone}
                onChange={(e) => setNewClient({...newClient, phone: e.target.value})}
                placeholder="(11) 99999-9999"
              />
            </div>
            <div className="form-group">
              <label>Status</label>
              <select
                value={newClient.status}
                onChange={(e) => setNewClient({...newClient, status: e.target.value})}
              >
                <option value="Ativo">Ativo</option>
                <option value="Inativo">Inativo</option>
              </select>
            </div>
            <div className="form-group">
              <button onClick={addClient} className="btn btn-primary">
                Adicionar Cliente
              </button>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Clientes Cadastrados</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Empresa</th>
                  <th>Contato</th>
                  <th>Email</th>
                  <th>Telefone</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {clients.map(client => (
                  <tr key={client.id}>
                    <td><strong>{client.name}</strong></td>
                    <td>{client.contact}</td>
                    <td>{client.email}</td>
                    <td>{client.phone}</td>
                    <td>
                      <span className={`status-badge status-${client.status.toLowerCase()}`}>
                        {client.status}
                      </span>
                    </td>
                    <td>
                      <button 
                        onClick={() => deleteClient(client.id)}
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

export default Sales;