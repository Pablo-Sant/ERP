import React, { useState, useEffect } from 'react';
import "../../styles/Module.css";
import salesApi from '../../services/salesAPI'; // Importar salesApi

const Sales = () => {
  // Estados para dados do banco
  const [sales, setSales] = useState([]);
  const [clients, setClients] = useState([]);
  const [contracts, setContracts] = useState([]); // Adicionando contratos
  const [loading, setLoading] = useState({
    sales: true,
    clients: true,
    contracts: true
  });
  const [error, setError] = useState(null);

  // Estados para formulários
  const [newSale, setNewSale] = useState({
    cliente_finalid: '',
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

  const [newContract, setNewContract] = useState({
    cliente_finalid: '',
    descricao: '',
    valor: '',
    data_inicio: '',
    data_fim: '',
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
        console.log('Resposta de clientes:', clientesResponse);
        
        // Ajuste para lidar com diferentes formatos de resposta
        let clientesData;
        if (Array.isArray(clientesResponse)) {
          clientesData = clientesResponse;
        } else if (clientesResponse && Array.isArray(clientesResponse.data)) {
          clientesData = clientesResponse.data;
        } else if (clientesResponse && clientesResponse.results) {
          clientesData = clientesResponse.results;
        } else {
          console.error('Formato de resposta inesperado:', clientesResponse);
          clientesData = [];
        }
        
        console.log('Dados formatados de clientes:', clientesData);
        
        const formattedClients = clientesData.map(cliente => ({
          id: cliente.id || cliente.cliente_finalid,
          nome: cliente.nome || cliente.name,
          email: cliente.email || '',
          telefone: cliente.telefone || cliente.phone || '',
          endereco: cliente.endereco || '',
          cnpj: cliente.cnpj || '',
          status: cliente.status || 'Ativo'
        }));
        
        setClients(formattedClients);
        setLoading(prev => ({ ...prev, clients: false }));
        
        // Carregar contratos (em vez de vendedores)
        console.log('Carregando contratos...');
        const contractsResponse = await salesApi.getContracts();
        console.log('Resposta de contratos:', contractsResponse);
        
        let contractsData;
        if (Array.isArray(contractsResponse)) {
          contractsData = contractsResponse;
        } else if (contractsResponse && Array.isArray(contractsResponse.data)) {
          contractsData = contractsResponse.data;
        } else {
          console.error('Formato de resposta inesperado:', contractsResponse);
          contractsData = [];
        }
        
        setContracts(contractsData);
        setLoading(prev => ({ ...prev, contracts: false }));
        
        // Carregar pedidos (vendas)
        console.log('Carregando pedidos...');
        const pedidosResponse = await salesApi.getSales();
        console.log('Resposta de pedidos:', pedidosResponse);
        
        let pedidosData;
        if (Array.isArray(pedidosResponse)) {
          pedidosData = pedidosResponse;
        } else if (pedidosResponse && Array.isArray(pedidosResponse.data)) {
          pedidosData = pedidosResponse.data;
        } else {
          console.error('Formato de resposta inesperado:', pedidosResponse);
          pedidosData = [];
        }
        
        // Transformar dados da API para o formato do frontend
        const transformedSales = pedidosData.map(pedido => {
          // Encontrar cliente correspondente
          const cliente = formattedClients.find(c => c.id === pedido.cliente_finalid);
          
          return {
            id: pedido.id || pedido.pedidoid,
            client: cliente?.nome || `Cliente ID: ${pedido.cliente_finalid}`,
            product: pedido.produto || 'Produto não especificado',
            value: pedido.valor_total 
              ? salesApi.formatCurrency(pedido.valor_total)
              : 'R$ 0,00',
            date: pedido.data_prevista_entrega 
              ? salesApi.formatDate(pedido.data_prevista_entrega)
              : salesApi.formatDate(new Date()),
            status: pedido.status || 'Proposta',
            cliente_id: pedido.cliente_finalid,
            observacoes: pedido.observacoes || '',
            // Para atualização completa (PUT)
            pedidoData: pedido
          };
        });
        
        setSales(transformedSales);
        setLoading(prev => ({ ...prev, sales: false }));
        
        console.log('Dados carregados com sucesso!');
        console.log('Clientes:', formattedClients.length);
        console.log('Contratos:', contractsData.length);
        console.log('Pedidos:', transformedSales.length);
        
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
        setError(`Erro ao carregar dados da API: ${error.message}. Verifique se o servidor está rodando.`);
        setLoading({ sales: false, clients: false, contracts: false });
      }
    };

    loadInitialData();
  }, []);

  const addSale = async () => {
    if (!newSale.cliente_finalid || !newSale.produto) {
      alert('Preencha todos os campos obrigatórios: Cliente e Produto');
      return;
    }

    try {
      // Converter valor para número
      let valorNumerico = 0;
      if (newSale.valor_total) {
        valorNumerico = salesApi.parseCurrency(newSale.valor_total);
      }

      const pedidoData = {
        cliente_finalid: parseInt(newSale.cliente_finalid),
        produto: newSale.produto,
        valor_total: valorNumerico,
        data_prevista_entrega: newSale.data_prevista_entrega || new Date().toISOString().split('T')[0],
        status: newSale.status,
        observacoes: newSale.observacoes || ''
      };

      console.log('Enviando pedido:', pedidoData);
      const response = await salesApi.createSale(pedidoData);
      console.log('Resposta do servidor:', response);
      
      const newSaleData = response.data || response;
      console.log('Pedido criado:', newSaleData);
      
      // Buscar cliente selecionado
      const cliente = clients.find(c => c.id === parseInt(newSale.cliente_finalid));
      
      const novaVenda = {
        id: newSaleData.id || newSaleData.pedidoid,
        client: cliente?.nome || `Cliente ID: ${newSaleData.cliente_finalid}`,
        product: newSaleData.produto,
        value: salesApi.formatCurrency(newSaleData.valor_total || 0),
        date: salesApi.formatDate(newSaleData.data_prevista_entrega),
        status: newSaleData.status,
        cliente_id: newSaleData.cliente_finalid,
        observacoes: newSaleData.observacoes || '',
        pedidoData: newSaleData
      };

      setSales([...sales, novaVenda]);
      
      // Limpar formulário
      setNewSale({
        cliente_finalid: '',
        produto: '',
        valor_total: '',
        data_prevista_entrega: '',
        status: 'Proposta',
        observacoes: ''
      });

      alert('Venda cadastrada com sucesso!');
      
    } catch (error) {
      console.error('Erro ao cadastrar venda:', error);
      const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message || 'Erro desconhecido';
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
      console.log('Resposta do servidor:', response);
      
      const newClientData = response.data || response;
      console.log('Cliente criado:', newClientData);
      
      const novoCliente = {
        id: newClientData.id || newClientData.cliente_finalid,
        nome: newClientData.nome,
        email: newClientData.email,
        telefone: newClientData.telefone || '',
        endereco: newClientData.endereco || '',
        cnpj: newClientData.cnpj || '',
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
      const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message || 'Erro desconhecido';
      alert(`Erro ao cadastrar cliente: ${errorMsg}`);
    }
  };

  const addContract = async () => {
    if (!newContract.cliente_finalid || !newContract.descricao || !newContract.valor) {
      alert('Preencha todos os campos obrigatórios: Cliente, Descrição e Valor');
      return;
    }

    try {
      const valorNumerico = salesApi.parseCurrency(newContract.valor);
      
      const contractData = {
        cliente_finalid: parseInt(newContract.cliente_finalid),
        descricao: newContract.descricao,
        valor: valorNumerico,
        data_inicio: newContract.data_inicio || new Date().toISOString().split('T')[0],
        data_fim: newContract.data_fim,
        status: newContract.status
      };

      console.log('Criando contrato:', contractData);
      const response = await salesApi.createContract(contractData);
      console.log('Contrato criado:', response);
      
      // Atualizar lista de contratos
      const contractsResponse = await salesApi.getContracts();
      let contractsData;
      if (Array.isArray(contractsResponse)) {
        contractsData = contractsResponse;
      } else if (contractsResponse && Array.isArray(contractsResponse.data)) {
        contractsData = contractsResponse.data;
      }
      
      if (contractsData) {
        setContracts(contractsData);
      }

      // Limpar formulário
      setNewContract({
        cliente_finalid: '',
        descricao: '',
        valor: '',
        data_inicio: '',
        data_fim: '',
        status: 'Ativo'
      });

      alert('Contrato cadastrado com sucesso!');
      
    } catch (error) {
      console.error('Erro ao cadastrar contrato:', error);
      const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message || 'Erro desconhecido';
      alert(`Erro ao cadastrar contrato: ${errorMsg}`);
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
      const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message || 'Erro desconhecido';
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
      const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message || 'Erro desconhecido';
      alert(`Erro ao excluir cliente: ${errorMsg}`);
    }
  };

  // Função para atualizar status usando updateSale (PUT completo)
  const updateSaleStatus = async (id, novoStatus) => {
    try {
      // Encontrar o pedido original
      const pedidoOriginal = sales.find(s => s.id === id);
      if (!pedidoOriginal || !pedidoOriginal.pedidoData) {
        throw new Error('Dados do pedido não encontrados');
      }

      // Criar objeto atualizado
      const updatedData = {
        ...pedidoOriginal.pedidoData,
        status: novoStatus
      };

      console.log('Atualizando pedido:', updatedData);
      
      // Usar updateSale (PUT)
      const response = await salesApi.updateSale(id, updatedData);
      const updatedSaleData = response.data || response;
      console.log('Pedido atualizado:', updatedSaleData);
      
      // Atualizar localmente
      setSales(sales.map(sale => {
        if (sale.id === id) {
          // Encontrar cliente
          const cliente = clients.find(c => c.id === updatedSaleData.cliente_finalid);
          
          return {
            ...sale,
            status: novoStatus,
            client: cliente?.nome || `Cliente ID: ${updatedSaleData.cliente_finalid}`,
            product: updatedSaleData.produto,
            value: salesApi.formatCurrency(updatedSaleData.valor_total || 0),
            date: salesApi.formatDate(updatedSaleData.data_prevista_entrega),
            pedidoData: updatedSaleData
          };
        }
        return sale;
      }));
      
      alert('Status atualizado com sucesso!');
    } catch (error) {
      console.error('Erro ao atualizar status:', error);
      const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message || 'Erro desconhecido';
      alert(`Erro ao atualizar status: ${errorMsg}`);
    }
  };

  // Calcular total de vendas fechadas
  const totalSales = sales
    .filter(sale => sale.status === 'Fechada')
    .reduce((sum, sale) => {
      const valor = salesApi.parseCurrency(sale.value);
      return sum + (isNaN(valor) ? 0 : valor);
    }, 0);

  // Calcular total de contratos ativos
  const totalActiveContracts = contracts
    .filter(contract => contract.status === 'Ativo')
    .reduce((sum, contract) => {
      return sum + (contract.valor || 0);
    }, 0);

  if (loading.sales || loading.clients || loading.contracts) {
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
            <h3>Vendas Fechadas</h3>
            <p className="amount">{salesApi.formatCurrency(totalSales)}</p>
          </div>
          <div className="summary-card">
            <h3>Total de Clientes</h3>
            <p className="count">{clients.length}</p>
          </div>
          <div className="summary-card">
            <h3>Contratos Ativos</h3>
            <p className="amount">{salesApi.formatCurrency(totalActiveContracts)}</p>
          </div>
          <div className="summary-card">
            <h3>Oportunidades</h3>
            <p className="opportunities">{sales.filter(s => s.status !== 'Fechada').length}</p>
          </div>
        </div>

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
                  <option key={client.id} value={client.id}>{client.nome}</option>
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
                  <th>Observações</th>
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
                      <td>{sale.observacoes || '-'}</td>
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
                  <th>CNPJ</th>
                  <th>Email</th>
                  <th>Telefone</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {clients.length === 0 ? (
                  <tr>
                    <td colSpan="6" style={{ textAlign: 'center', padding: '20px' }}>
                      Nenhum cliente cadastrado ainda.
                    </td>
                  </tr>
                ) : (
                  clients.map(client => (
                    <tr key={client.id}>
                      <td>
                        <strong>{client.nome}</strong>
                        <div className="contact-name">{client.endereco || 'Sem endereço'}</div>
                      </td>
                      <td>{client.cnpj || '-'}</td>
                      <td>{client.email}</td>
                      <td>{client.telefone || '-'}</td>
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

        {/* Formulário de Contratos */}
        <div className="card">
          <h2>Cadastro de Contratos</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Cliente *</label>
              <select
                value={newContract.cliente_finalid}
                onChange={(e) => setNewContract({...newContract, cliente_finalid: e.target.value})}
                required
              >
                <option value="">Selecione um cliente</option>
                {clients.map(client => (
                  <option key={client.id} value={client.id}>{client.nome}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Descrição *</label>
              <input
                type="text"
                value={newContract.descricao}
                onChange={(e) => setNewContract({...newContract, descricao: e.target.value})}
                placeholder="Descrição do contrato"
                required
              />
            </div>
            <div className="form-group">
              <label>Valor *</label>
              <input
                type="text"
                value={newContract.valor}
                onChange={(e) => setNewContract({...newContract, valor: e.target.value})}
                placeholder="R$ 0,00"
                required
              />
            </div>
            <div className="form-group">
              <label>Data Início</label>
              <input
                type="date"
                value={newContract.data_inicio}
                onChange={(e) => setNewContract({...newContract, data_inicio: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Data Fim</label>
              <input
                type="date"
                value={newContract.data_fim}
                onChange={(e) => setNewContract({...newContract, data_fim: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Status</label>
              <select
                value={newContract.status}
                onChange={(e) => setNewContract({...newContract, status: e.target.value})}
              >
                <option value="Ativo">Ativo</option>
                <option value="Inativo">Inativo</option>
                <option value="Pendente">Pendente</option>
              </select>
            </div>
            <div className="form-group">
              <button onClick={addContract} className="btn btn-primary">
                Adicionar Contrato
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sales;