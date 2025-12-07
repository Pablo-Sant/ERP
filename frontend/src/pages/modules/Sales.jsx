import React, { useState, useEffect } from 'react';
import "../../styles/Module.css";
import salesApi from '../../services/salesAPI'; // Importar salesApi

const Sales = () => {
  // Estados para dados do banco
  const [sales, setSales] = useState([]);
  const [clients, setClients] = useState([]);
  const [vendedores, setVendedores] = useState([]);
  const [loading, setLoading] = useState({
    sales: true,
    clients: true,
    vendedores: true
  });
  const [error, setError] = useState(null);

  // Estados para formulários
  const [newSale, setNewSale] = useState({
    cliente_finalid: '',
    vendedorid: '',
    produto: '',
    valor_total: '',
    data_prevista_entrega: '',
    status: 'Proposta',
    observacoes: ''
  });

  const [newClient, setNewClient] = useState({
    nome: '',
    cnpj: '',
    email: '',
    telefone: '',
    endereco: '',
    status: 'Ativo'
  });

  // Carregar dados da API
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        setError(null);
        console.log('Iniciando carregamento de dados...');
        
        // Carregar clientes
        console.log('Carregando clientes...');
        const clientesResponse = await salesApi.getClients();
        const clientesData = clientesResponse.data || clientesResponse;
        console.log('Clientes carregados:', clientesData);
        
        const formattedClients = clientesData.map(cliente => ({
          id: cliente.cliente_finalid,
          name: cliente.nome,
          contact: cliente.contato || cliente.nome,
          email: cliente.email,
          phone: cliente.telefone || '',
          status: cliente.status || 'Ativo'
        }));
        
        setClients(formattedClients);
        setLoading(prev => ({ ...prev, clients: false }));
        
        // Carregar vendedores
        console.log('Carregando vendedores...');
        const vendedoresResponse = await salesApi.getSellers();
        const vendedoresData = vendedoresResponse.data || vendedoresResponse;
        console.log('Vendedores carregados:', vendedoresData);
        
        setVendedores(vendedoresData);
        setLoading(prev => ({ ...prev, vendedores: false }));
        
        // Carregar pedidos (vendas)
        console.log('Carregando pedidos...');
        const pedidosResponse = await salesApi.getSales();
        const pedidosData = pedidosResponse.data || pedidosResponse;
        console.log('Pedidos carregados:', pedidosData);
        
        // Transformar dados da API para o formato do frontend
        const transformedSales = pedidosData.map(pedido => {
          // Encontrar cliente correspondente
          const cliente = clientesData.find(c => c.cliente_finalid === pedido.cliente_finalid);
          // Encontrar vendedor correspondente
          const vendedor = vendedoresData.find(v => v.vendedorid === pedido.vendedorid);
          
          return {
            id: pedido.pedidoid,
            client: cliente?.nome || `Cliente ID: ${pedido.cliente_finalid}`,
            product: pedido.produto || 'Produto não especificado',
            value: `R$ ${parseFloat(pedido.valor_total || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`,
            date: pedido.data_prevista_entrega 
              ? new Date(pedido.data_prevista_entrega).toISOString().split('T')[0]
              : new Date().toISOString().split('T')[0],
            status: pedido.status || 'Proposta',
            seller: vendedor?.nome || `Vendedor ID: ${pedido.vendedorid}`,
            cliente_id: pedido.cliente_finalid,
            vendedor_id: pedido.vendedorid
          };
        });
        
        setSales(transformedSales);
        setLoading(prev => ({ ...prev, sales: false }));
        
        console.log('Dados carregados com sucesso!');
        
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
        setError(`Erro ao carregar dados da API: ${error.message}. Verifique se o servidor está rodando.`);
        setLoading({ sales: false, clients: false, vendedores: false });
      }
    };

    loadInitialData();
  }, []);

  const addSale = async () => {
    if (!newSale.cliente_finalid || !newSale.vendedorid || !newSale.produto) {
      alert('Preencha todos os campos obrigatórios: Cliente, Vendedor e Produto');
      return;
    }

    try {
      // Converter valor para número
      let valorNumerico = 0;
      if (newSale.valor_total) {
        // Remove "R$ " e converte para número
        const valorLimpo = newSale.valor_total
          .replace('R$ ', '')
          .replace(/\./g, '')
          .replace(',', '.');
        valorNumerico = parseFloat(valorLimpo);
        if (isNaN(valorNumerico)) valorNumerico = 0;
      }

      const pedidoData = {
        cliente_finalid: parseInt(newSale.cliente_finalid),
        vendedorid: parseInt(newSale.vendedorid),
        produto: newSale.produto,
        valor_total: valorNumerico,
        data_prevista_entrega: newSale.data_prevista_entrega || new Date().toISOString().split('T')[0],
        status: newSale.status,
        observacoes: newSale.observacoes || ''
      };

      console.log('Enviando pedido:', pedidoData);
      const response = await salesApi.createSale(pedidoData);
      const newSaleData = response.data || response;
      console.log('Pedido criado:', newSaleData);
      
      // Buscar cliente e vendedor selecionados
      const cliente = clients.find(c => c.id === parseInt(newSale.cliente_finalid));
      const vendedor = vendedores.find(v => v.vendedorid === parseInt(newSale.vendedorid));
      
      const novaVenda = {
        id: newSaleData.pedidoid,
        client: cliente?.name || `Cliente ID: ${newSaleData.cliente_finalid}`,
        product: newSaleData.produto,
        value: `R$ ${valorNumerico.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`,
        date: newSaleData.data_prevista_entrega,
        status: newSaleData.status,
        seller: vendedor?.nome || `Vendedor ID: ${newSaleData.vendedorid}`,
        cliente_id: newSaleData.cliente_finalid,
        vendedor_id: newSaleData.vendedorid
      };

      setSales([...sales, novaVenda]);
      
      // Limpar formulário
      setNewSale({
        cliente_finalid: '',
        vendedorid: '',
        produto: '',
        valor_total: '',
        data_prevista_entrega: '',
        status: 'Proposta',
        observacoes: ''
      });

      alert('Venda cadastrada com sucesso!');
      
    } catch (error) {
      console.error('Erro ao cadastrar venda:', error);
      const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message;
      alert(`Erro ao cadastrar venda: ${errorMsg}`);
    }
  };

  const addClient = async () => {
    if (!newClient.nome || !newClient.email) {
      alert('Preencha os campos obrigatórios: Nome e Email');
      return;
    }

    try {
      console.log('Criando cliente:', newClient);
      const response = await salesApi.createClient(newClient);
      const newClientData = response.data || response;
      console.log('Cliente criado:', newClientData);
      
      const novoCliente = {
        id: newClientData.cliente_finalid,
        name: newClientData.nome,
        contact: newClientData.contato || newClientData.nome,
        email: newClientData.email,
        phone: newClientData.telefone || '',
        status: newClientData.status || 'Ativo'
      };

      setClients([...clients, novoCliente]);
      
      // Limpar formulário
      setNewClient({
        nome: '',
        cnpj: '',
        email: '',
        telefone: '',
        endereco: '',
        status: 'Ativo'
      });

      alert('Cliente cadastrado com sucesso!');
      
    } catch (error) {
      console.error('Erro ao cadastrar cliente:', error);
      const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message;
      alert(`Erro ao cadastrar cliente: ${errorMsg}`);
    }
  };

  const deleteSale = async (id) => {
    if (!window.confirm('Tem certeza que deseja excluir esta venda?')) {
      return;
    }

    try {
      await salesApi.deleteSale(id);
      setSales(sales.filter(sale => sale.id !== id));
      alert('Venda excluída com sucesso!');
    } catch (error) {
      console.error('Erro ao excluir venda:', error);
      const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message;
      alert(`Erro ao excluir venda: ${errorMsg}`);
    }
  };

  const deleteClient = async (id) => {
    if (!window.confirm('Tem certeza que deseja excluir este cliente?')) {
      return;
    }

    try {
      await salesApi.deleteClient(id);
      setClients(clients.filter(client => client.id !== id));
      alert('Cliente excluído com sucesso!');
    } catch (error) {
      console.error('Erro ao excluir cliente:', error);
      const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message;
      alert(`Erro ao excluir cliente: ${errorMsg}`);
    }
  };

  const updateSaleStatus = async (id, novoStatus) => {
    try {
      await salesApi.updateSaleStatus(id, novoStatus);
      
      setSales(sales.map(sale => 
        sale.id === id ? { ...sale, status: novoStatus } : sale
      ));
      
      alert('Status atualizado com sucesso!');
    } catch (error) {
      console.error('Erro ao atualizar status:', error);
      const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message;
      alert(`Erro ao atualizar status: ${errorMsg}`);
    }
  };

  // Calcular total de vendas
  const totalSales = sales
    .filter(sale => sale.status === 'Fechada')
    .reduce((sum, sale) => {
      const valor = parseFloat(sale.value.replace('R$ ', '').replace(/\./g, '').replace(',', '.'));
      return sum + (isNaN(valor) ? 0 : valor);
    }, 0);

  if (loading.sales || loading.clients || loading.vendedores) {
    return (
      <div className="module">
        <div className="module-header">
          <h1>Vendas</h1>
          <p>Gestão comercial e CRM</p>
        </div>
        <div className="module-content">
          <div className="loading">
            <p>Carregando dados...</p>
            {error && <p className="error-message">{error}</p>}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="module">
      <div className="module-header">
        <h1>Vendas</h1>
        <p>Gestão comercial e CRM</p>
      </div>

      {error && (
        <div className="alert alert-error">
          <p>{error}</p>
          <button onClick={() => window.location.reload()} className="btn btn-sm">
            Tentar novamente
          </button>
        </div>
      )}

      <div className="module-content">
        {/* Cards de Resumo */}
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

        {/* Resto do seu JSX continua aqui... */}
        {/* Formulário de Nova Venda */}
        <div className="card">
          <h2>Nova Venda/Oportunidade</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Cliente *</label>
              <select
                value={newSale.cliente_finalid}
                onChange={(e) => setNewSale({...newSale, cliente_finalid: e.target.value})}
                required
              >
                <option value="">Selecione um cliente</option>
                {clients.map(client => (
                  <option key={client.id} value={client.id}>{client.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Vendedor *</label>
              <select
                value={newSale.vendedorid}
                onChange={(e) => setNewSale({...newSale, vendedorid: e.target.value})}
                required
              >
                <option value="">Selecione um vendedor</option>
                {vendedores.map(vendedor => (
                  <option key={vendedor.vendedorid} value={vendedor.vendedorid}>
                    {vendedor.nome}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Produto/Serviço *</label>
              <input
                type="text"
                value={newSale.produto}
                onChange={(e) => setNewSale({...newSale, produto: e.target.value})}
                placeholder="Descrição do produto/serviço"
                required
              />
            </div>
            <div className="form-group">
              <label>Valor</label>
              <input
                type="text"
                value={newSale.valor_total}
                onChange={(e) => setNewSale({...newSale, valor_total: e.target.value})}
                placeholder="R$ 0,00"
              />
            </div>
            <div className="form-group">
              <label>Data Prevista</label>
              <input
                type="date"
                value={newSale.data_prevista_entrega}
                onChange={(e) => setNewSale({...newSale, data_prevista_entrega: e.target.value})}
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
                <option value="Cancelada">Cancelada</option>
              </select>
            </div>
            <div className="form-group">
              <label>Observações</label>
              <textarea
                value={newSale.observacoes}
                onChange={(e) => setNewSale({...newSale, observacoes: e.target.value})}
                placeholder="Observações adicionais..."
                rows="3"
              />
            </div>
            <div className="form-group">
              <button onClick={addSale} className="btn btn-primary">
                Adicionar Venda
              </button>
            </div>
          </div>
        </div>

        {/* Pipeline de Vendas */}
        <div className="card">
          <h2>Pipeline de Vendas</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Cliente</th>
                  <th>Produto/Serviço</th>
                  <th>Valor</th>
                  <th>Data Prevista</th>
                  <th>Status</th>
                  <th>Vendedor</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {sales.length === 0 ? (
                  <tr>
                    <td colSpan="7" style={{ textAlign: 'center', padding: '20px' }}>
                      Nenhuma venda cadastrada ainda.
                    </td>
                  </tr>
                ) : (
                  sales.map(sale => (
                    <tr key={sale.id}>
                      <td><strong>{sale.client}</strong></td>
                      <td>{sale.product}</td>
                      <td>{sale.value}</td>
                      <td>{sale.date}</td>
                      <td>
                        <select
                          value={sale.status}
                          onChange={(e) => updateSaleStatus(sale.id, e.target.value)}
                          className={`status-select status-${sale.status.toLowerCase()}`}
                        >
                          <option value="Proposta">Proposta</option>
                          <option value="Negociação">Negociação</option>
                          <option value="Fechada">Fechada</option>
                          <option value="Perdida">Perdida</option>
                          <option value="Cancelada">Cancelada</option>
                        </select>
                      </td>
                      <td>{sale.seller}</td>
                      <td>
                        <div className="action-buttons">
                          <button 
                            onClick={() => deleteSale(sale.id)}
                            className="btn btn-danger btn-sm"
                          >
                            Excluir
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Formulário de Cadastro de Clientes */}
        <div className="card">
          <h2>Cadastro de Clientes</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Nome/Razão Social *</label>
              <input
                type="text"
                value={newClient.nome}
                onChange={(e) => setNewClient({...newClient, nome: e.target.value})}
                placeholder="Nome ou razão social"
                required
              />
            </div>
            <div className="form-group">
              <label>CNPJ</label>
              <input
                type="text"
                value={newClient.cnpj}
                onChange={(e) => setNewClient({...newClient, cnpj: e.target.value})}
                placeholder="00.000.000/0000-00"
              />
            </div>
            <div className="form-group">
              <label>Email *</label>
              <input
                type="email"
                value={newClient.email}
                onChange={(e) => setNewClient({...newClient, email: e.target.value})}
                placeholder="email@empresa.com"
                required
              />
            </div>
            <div className="form-group">
              <label>Telefone</label>
              <input
                type="text"
                value={newClient.telefone}
                onChange={(e) => setNewClient({...newClient, telefone: e.target.value})}
                placeholder="(11) 99999-9999"
              />
            </div>
            <div className="form-group">
              <label>Endereço</label>
              <input
                type="text"
                value={newClient.endereco}
                onChange={(e) => setNewClient({...newClient, endereco: e.target.value})}
                placeholder="Endereço completo"
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
                <option value="Potencial">Potencial</option>
              </select>
            </div>
            <div className="form-group">
              <button onClick={addClient} className="btn btn-primary">
                Adicionar Cliente
              </button>
            </div>
          </div>
        </div>

        {/* Lista de Clientes Cadastrados */}
        <div className="card">
          <h2>Clientes Cadastrados</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Empresa</th>
                  <th>Email</th>
                  <th>Telefone</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {clients.length === 0 ? (
                  <tr>
                    <td colSpan="5" style={{ textAlign: 'center', padding: '20px' }}>
                      Nenhum cliente cadastrado ainda.
                    </td>
                  </tr>
                ) : (
                  clients.map(client => (
                    <tr key={client.id}>
                      <td>
                        <strong>{client.name}</strong>
                        {client.contact !== client.name && (
                          <div className="contact-name">{client.contact}</div>
                        )}
                      </td>
                      <td>{client.email}</td>
                      <td>{client.phone}</td>
                      <td>
                        <span className={`status-badge status-${(client.status || 'Ativo').toLowerCase()}`}>
                          {client.status || 'Ativo'}
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
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sales;