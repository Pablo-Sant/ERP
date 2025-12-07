import React, { useState, useEffect } from 'react';
import "../../styles/Module.css";

const API_BASE_URL = 'http://localhost:8000/api/ativos';

const AssetManagement = () => {
  const [assets, setAssets] = useState([]);
  const [categories, setCategories] = useState([]);
  const [locations, setLocations] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [activeTab, setActiveTab] = useState('ativos');

  const [newAsset, setNewAsset] = useState({
    numero_tag: '',
    nome: '',
    id_categoria: '',
    id_localizacao: '',
    id_fornecedor: '',
    numero_serie: '',
    modelo: '',
    fabricante: '',
    descricao: '',
    status_ativo: 'ativo',
    criticidade: 'medio',
    data_aquisicao: '',
    custo_aquisicao: '',
    numero_ordem_compra: '',
    data_vencimento_garantia: '',
    vida_util_anos: '',
    valor_residual: '',
    valor_atual: '',
    observacoes: ''
  });

  // Carregar dados da API
  useEffect(() => {
    fetchAssets();
    fetchDashboardData();
    fetchCategories();
    fetchLocations();
    fetchSuppliers();
  }, []);

  const fetchAssets = async () => {
    try {
      setLoading(true);
      const response = await fetch(API_BASE_URL);
      if (!response.ok) throw new Error('Erro ao carregar ativos');
      const data = await response.json();
      setAssets(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Erro ao buscar ativos:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchDashboardData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/dashboard/resumo`);
      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
      }
    } catch (err) {
      console.error('Erro ao buscar dashboard:', err);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/categorias/listar`);
      if (response.ok) {
        const data = await response.json();
        setCategories(data);
      }
    } catch (err) {
      console.error('Erro ao buscar categorias:', err);
    }
  };

  const fetchLocations = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/localizacoes/listar`);
      if (response.ok) {
        const data = await response.json();
        setLocations(data);
      }
    } catch (err) {
      console.error('Erro ao buscar localizações:', err);
    }
  };

  const fetchSuppliers = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/fornecedores/listar`);
      if (response.ok) {
        const data = await response.json();
        setSuppliers(data);
      }
    } catch (err) {
      console.error('Erro ao buscar fornecedores:', err);
    }
  };

  const addAsset = async () => {
    if (!newAsset.nome || !newAsset.numero_tag || !newAsset.id_categoria || !newAsset.id_localizacao) {
      alert('Por favor, preencha os campos obrigatórios: Nome, Tag, Categoria e Localização');
      return;
    }

    try {
      const assetToSend = {
        ...newAsset,
        custo_aquisicao: newAsset.custo_aquisicao ? parseFloat(newAsset.custo_aquisicao) : 0,
        valor_atual: newAsset.valor_atual ? parseFloat(newAsset.valor_atual) : 
                   (newAsset.custo_aquisicao ? parseFloat(newAsset.custo_aquisicao) : 0),
        valor_residual: newAsset.valor_residual ? parseFloat(newAsset.valor_residual) : 0,
        vida_util_anos: newAsset.vida_util_anos ? parseInt(newAsset.vida_util_anos) : null,
        id_fornecedor: newAsset.id_fornecedor || null
      };

      const response = await fetch(API_BASE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(assetToSend),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erro ao adicionar ativo');
      }

      const createdAsset = await response.json();
      setAssets([createdAsset, ...assets]);
      
      // Reset form
      setNewAsset({
        numero_tag: '',
        nome: '',
        id_categoria: '',
        id_localizacao: '',
        id_fornecedor: '',
        numero_serie: '',
        modelo: '',
        fabricante: '',
        descricao: '',
        status_ativo: 'ativo',
        criticidade: 'medio',
        data_aquisicao: '',
        custo_aquisicao: '',
        numero_ordem_compra: '',
        data_vencimento_garantia: '',
        vida_util_anos: '',
        valor_residual: '',
        valor_atual: '',
        observacoes: ''
      });

      fetchDashboardData();
      alert('Ativo adicionado com sucesso!');
    } catch (err) {
      setError(err.message);
      alert(`Erro: ${err.message}`);
    }
  };

  const deleteAsset = async (id) => {
    if (!window.confirm('Tem certeza que deseja excluir este ativo?')) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Erro ao excluir ativo');
      }

      setAssets(assets.filter(asset => asset.id !== id));
      fetchDashboardData();
      alert('Ativo excluído com sucesso!');
    } catch (err) {
      setError(err.message);
      alert(`Erro: ${err.message}`);
    }
  };

  const formatCurrency = (value) => {
    if (value === null || value === undefined) return 'R$ 0,00';
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 2
    }).format(value);
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const formatStatus = (status) => {
    const statusMap = {
      'ativo': 'Ativo',
      'inativo': 'Inativo',
      'em_manutencao': 'Em Manutenção',
      'baixado': 'Baixado',
      'planejado': 'Planejado',
      'descartado': 'Descartado',
      'perdido': 'Perdido'
    };
    return statusMap[status] || status;
  };

  const getStatusBadgeClass = (status) => {
    const classMap = {
      'ativo': 'status-ativo',
      'inativo': 'status-inativo',
      'em_manutencao': 'status-manutencao',
      'baixado': 'status-baixado',
      'planejado': 'status-planejado',
      'descartado': 'status-descartado',
      'perdido': 'status-perdido'
    };
    return classMap[status] || 'status-ativo';
  };

  const getCriticidadeClass = (criticidade) => {
    const classMap = {
      'baixa': 'criticidade-baixa',
      'medio': 'criticidade-medio',
      'alta': 'criticidade-alta',
      'critico': 'criticidade-critico'
    };
    return classMap[criticidade] || 'criticidade-medio';
  };

  if (loading) {
    return (
      <div className="module">
        <div className="module-header">
          <h1>Gestão de Ativos</h1>
          <p>Controle de patrimônio</p>
        </div>
        <div className="module-content">
          <div className="loading-spinner">
            <p>Carregando ativos...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="module">
      <div className="module-header">
        <h1>Gestão de Ativos</h1>
        <p>Controle de patrimônio</p>
        {error && (
          <div className="alert alert-danger">
            <strong>Erro:</strong> {error}
            <button onClick={() => setError(null)} className="btn-close"></button>
          </div>
        )}
      </div>

      <div className="tabs">
        <button 
          className={`tab-btn ${activeTab === 'ativos' ? 'active' : ''}`}
          onClick={() => setActiveTab('ativos')}
        >
          Ativos
        </button>
        <button 
          className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          Dashboard
        </button>
        <button 
          className={`tab-btn ${activeTab === 'cadastro' ? 'active' : ''}`}
          onClick={() => setActiveTab('cadastro')}
        >
          Novo Ativo
        </button>
      </div>

      <div className="module-content">
        {activeTab === 'dashboard' && dashboardData && (
          <>
            {/* Dashboard Cards */}
            <div className="asset-summary">
              <div className="summary-card">
                <h3>Total de Ativos</h3>
                <p className="count">{dashboardData.total_ativos}</p>
              </div>
              <div className="summary-card">
                <h3>Valor Total</h3>
                <p className="value">{formatCurrency(dashboardData.valor_total)}</p>
              </div>
              <div className="summary-card">
                <h3>Categorias</h3>
                <p className="categories">{dashboardData.total_categorias}</p>
              </div>
              <div className="summary-card">
                <h3>Status Ativos</h3>
                <p className="count">
                  {dashboardData.ativos_por_status?.find(s => s.status === 'ativo')?.quantidade || 0}
                </p>
              </div>
            </div>

            {/* Estatísticas Detalhadas */}
            <div className="card">
              <h2>Estatísticas Detalhadas</h2>
              <div className="stats-grid">
                <div className="stats-card">
                  <h4>Ativos por Status</h4>
                  <ul className="stats-list">
                    {dashboardData.ativos_por_status?.map((item, index) => (
                      <li key={index}>
                        <span className="stat-label">{formatStatus(item.status)}:</span>
                        <span className="stat-value">{item.quantidade} ({formatCurrency(item.valor_total)})</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="stats-card">
                  <h4>Ativos por Categoria</h4>
                  <ul className="stats-list">
                    {dashboardData.ativos_por_categoria?.slice(0, 5).map((item, index) => (
                      <li key={index}>
                        <span className="stat-label">{item.categoria}:</span>
                        <span className="stat-value">{item.quantidade} ({formatCurrency(item.valor_total)})</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="stats-card">
                  <h4>Ativos por Criticidade</h4>
                  <ul className="stats-list">
                    {dashboardData.ativos_por_criticidade?.map((item, index) => (
                      <li key={index}>
                        <span className="stat-label">{item.criticidade}:</span>
                        <span className="stat-value">{item.quantidade} ({formatCurrency(item.valor_total)})</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </>
        )}

        {activeTab === 'cadastro' && (
          <div className="card">
            <h2>Novo Ativo</h2>
            <div className="form-grid">
              <div className="form-group">
                <label>Tag/Número *</label>
                <input
                  type="text"
                  value={newAsset.numero_tag}
                  onChange={(e) => setNewAsset({...newAsset, numero_tag: e.target.value})}
                  placeholder="Ex: ATV-001"
                  required
                />
              </div>
              <div className="form-group">
                <label>Nome do Ativo *</label>
                <input
                  type="text"
                  value={newAsset.nome}
                  onChange={(e) => setNewAsset({...newAsset, nome: e.target.value})}
                  placeholder="Nome descritivo do ativo"
                  required
                />
              </div>
              <div className="form-group">
                <label>Categoria *</label>
                <select
                  value={newAsset.id_categoria}
                  onChange={(e) => setNewAsset({...newAsset, id_categoria: e.target.value})}
                  required
                >
                  <option value="">Selecione...</option>
                  {categories.map(cat => (
                    <option key={cat.id} value={cat.id}>{cat.nome}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Localização *</label>
                <select
                  value={newAsset.id_localizacao}
                  onChange={(e) => setNewAsset({...newAsset, id_localizacao: e.target.value})}
                  required
                >
                  <option value="">Selecione...</option>
                  {locations.map(loc => (
                    <option key={loc.id} value={loc.id}>{loc.nome}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Fornecedor</label>
                <select
                  value={newAsset.id_fornecedor}
                  onChange={(e) => setNewAsset({...newAsset, id_fornecedor: e.target.value})}
                >
                  <option value="">Selecione...</option>
                  {suppliers.map(sup => (
                    <option key={sup.id} value={sup.id}>{sup.nome}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Número de Série</label>
                <input
                  type="text"
                  value={newAsset.numero_serie}
                  onChange={(e) => setNewAsset({...newAsset, numero_serie: e.target.value})}
                  placeholder="Número de série"
                />
              </div>
              <div className="form-group">
                <label>Modelo</label>
                <input
                  type="text"
                  value={newAsset.modelo}
                  onChange={(e) => setNewAsset({...newAsset, modelo: e.target.value})}
                  placeholder="Modelo do equipamento"
                />
              </div>
              <div className="form-group">
                <label>Fabricante</label>
                <input
                  type="text"
                  value={newAsset.fabricante}
                  onChange={(e) => setNewAsset({...newAsset, fabricante: e.target.value})}
                  placeholder="Fabricante"
                />
              </div>
              <div className="form-group">
                <label>Data Aquisição</label>
                <input
                  type="date"
                  value={newAsset.data_aquisicao}
                  onChange={(e) => setNewAsset({...newAsset, data_aquisicao: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Custo de Aquisição (R$)</label>
                <input
                  type="number"
                  step="0.01"
                  value={newAsset.custo_aquisicao}
                  onChange={(e) => setNewAsset({...newAsset, custo_aquisicao: e.target.value})}
                  placeholder="0.00"
                />
              </div>
              <div className="form-group">
                <label>Valor Atual (R$)</label>
                <input
                  type="number"
                  step="0.01"
                  value={newAsset.valor_atual}
                  onChange={(e) => setNewAsset({...newAsset, valor_atual: e.target.value})}
                  placeholder="0.00"
                />
              </div>
              <div className="form-group">
                <label>Número Ordem de Compra</label>
                <input
                  type="text"
                  value={newAsset.numero_ordem_compra}
                  onChange={(e) => setNewAsset({...newAsset, numero_ordem_compra: e.target.value})}
                  placeholder="Número da OC"
                />
              </div>
              <div className="form-group">
                <label>Vencimento Garantia</label>
                <input
                  type="date"
                  value={newAsset.data_vencimento_garantia}
                  onChange={(e) => setNewAsset({...newAsset, data_vencimento_garantia: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Vida Útil (anos)</label>
                <input
                  type="number"
                  value={newAsset.vida_util_anos}
                  onChange={(e) => setNewAsset({...newAsset, vida_util_anos: e.target.value})}
                  placeholder="5"
                />
              </div>
              <div className="form-group">
                <label>Valor Residual (R$)</label>
                <input
                  type="number"
                  step="0.01"
                  value={newAsset.valor_residual}
                  onChange={(e) => setNewAsset({...newAsset, valor_residual: e.target.value})}
                  placeholder="0.00"
                />
              </div>
              <div className="form-group">
                <label>Status</label>
                <select
                  value={newAsset.status_ativo}
                  onChange={(e) => setNewAsset({...newAsset, status_ativo: e.target.value})}
                >
                  <option value="ativo">Ativo</option>
                  <option value="inativo">Inativo</option>
                  <option value="em_manutencao">Em Manutenção</option>
                  <option value="baixado">Baixado</option>
                  <option value="planejado">Planejado</option>
                </select>
              </div>
              <div className="form-group">
                <label>Criticidade</label>
                <select
                  value={newAsset.criticidade}
                  onChange={(e) => setNewAsset({...newAsset, criticidade: e.target.value})}
                >
                  <option value="baixa">Baixa</option>
                  <option value="medio">Média</option>
                  <option value="alta">Alta</option>
                  <option value="critico">Crítico</option>
                </select>
              </div>
              <div className="form-group full-width">
                <label>Descrição</label>
                <textarea
                  value={newAsset.descricao}
                  onChange={(e) => setNewAsset({...newAsset, descricao: e.target.value})}
                  placeholder="Descrição detalhada do ativo"
                  rows="3"
                />
              </div>
              <div className="form-group full-width">
                <label>Observações</label>
                <textarea
                  value={newAsset.observacoes}
                  onChange={(e) => setNewAsset({...newAsset, observacoes: e.target.value})}
                  placeholder="Observações adicionais"
                  rows="2"
                />
              </div>
              <div className="form-group">
                <button onClick={addAsset} className="btn btn-primary">
                  Adicionar Ativo
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'ativos' && (
          <div className="card">
            <div className="card-header">
              <h2>Inventário de Ativos ({assets.length})</h2>
              <div>
                <button onClick={fetchAssets} className="btn btn-secondary btn-sm mr-2">
                  Atualizar
                </button>
              </div>
            </div>
            <div className="table-container">
              {assets.length === 0 ? (
                <div className="alert alert-info">
                  Nenhum ativo cadastrado. Adicione seu primeiro ativo usando o formulário acima.
                </div>
              ) : (
                <table>
                  <thead>
                    <tr>
                      <th>Tag</th>
                      <th>Nome</th>
                      <th>Categoria</th>
                      <th>Localização</th>
                      <th>Aquisição</th>
                      <th>Valor</th>
                      <th>Status</th>
                      <th>Criticidade</th>
                      <th>Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {assets.map(asset => (
                      <tr key={asset.id}>
                        <td><strong>{asset.numero_tag}</strong></td>
                        <td>
                          <div>{asset.nome}</div>
                          {asset.modelo && <small className="text-muted">{asset.modelo}</small>}
                        </td>
                        <td>{asset.categoria_nome || `Categoria ${asset.id_categoria}`}</td>
                        <td>{asset.localizacao_nome || `Local ${asset.id_localizacao}`}</td>
                        <td>{formatDate(asset.data_aquisicao)}</td>
                        <td>{formatCurrency(asset.valor_atual || asset.custo_aquisicao)}</td>
                        <td>
                          <span className={`status-badge ${getStatusBadgeClass(asset.status_ativo)}`}>
                            {formatStatus(asset.status_ativo)}
                          </span>
                        </td>
                        <td>
                          <span className={`criticidade-badge ${getCriticidadeClass(asset.criticidade)}`}>
                            {asset.criticidade}
                          </span>
                        </td>
                        <td>
                          <button 
                            onClick={() => deleteAsset(asset.id)}
                            className="btn btn-danger btn-sm"
                            title="Excluir ativo"
                          >
                            Excluir
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AssetManagement;