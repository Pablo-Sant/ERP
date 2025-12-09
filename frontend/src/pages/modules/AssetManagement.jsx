import React, { useState, useEffect } from 'react';
import assetAPI from '../../services/assetAPI'; // Importando a API criada
import "../../styles/Module.css";

const AssetManagement = () => {
  const [assets, setAssets] = useState([]);
  const [categories, setCategories] = useState([]);
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [activeTab, setActiveTab] = useState('ativos');
  const [statistics, setStatistics] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [maintenanceAlerts, setMaintenanceAlerts] = useState([]);
  const [warrantyAlerts, setWarrantyAlerts] = useState([]);

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
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      await Promise.all([
        fetchAssets(),
        fetchDashboardData(),
        fetchCategories(),
        fetchLocations(),
        fetchStatistics(),
        fetchAlerts(),
        fetchMaintenanceAlerts(),
        fetchWarrantyAlerts()
      ]);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Erro ao carregar dados:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAssets = async () => {
    try {
      const data = await assetAPI.getAssets({ 
        limit: 100,
        order_by: 'data_criacao',
        order_direction: 'desc'
      });
      setAssets(data || []);
    } catch (err) {
      console.error('Erro ao buscar ativos:', err);
      throw err;
    }
  };

  const fetchDashboardData = async () => {
    try {
      const data = await assetAPI.getAssetDashboard();
      setDashboardData(data);
    } catch (err) {
      console.error('Erro ao buscar dashboard:', err);
      // Fallback para dados simulados
      setDashboardData({
        total_ativos: assets.length,
        valor_total: assets.reduce((sum, asset) => sum + (asset.valor_atual || asset.custo_aquisicao || 0), 0),
        total_categorias: categories.length,
        ativos_por_status: [],
        ativos_por_categoria: [],
        ativos_por_criticidade: []
      });
    }
  };

  const fetchCategories = async () => {
    try {
      const data = await assetAPI.getCategories({ 
        status: 'ativo',
        order_by: 'nome'
      });
      setCategories(data || []);
    } catch (err) {
      console.error('Erro ao buscar categorias:', err);
    }
  };

  const fetchLocations = async () => {
    try {
      const data = await assetAPI.getLocations({ 
        status: 'ativo',
        order_by: 'nome'
      });
      setLocations(data || []);
    } catch (err) {
      console.error('Erro ao buscar localizações:', err);
    }
  };

  const fetchStatistics = async () => {
    try {
      const data = await assetAPI.getAssetStatistics();
      setStatistics(data);
    } catch (err) {
      console.error('Erro ao buscar estatísticas:', err);
    }
  };

  const fetchAlerts = async () => {
    try {
      const data = await assetAPI.getAssetAlerts({ limit: 10 });
      setAlerts(data || []);
    } catch (err) {
      console.error('Erro ao buscar alertas:', err);
    }
  };

  const fetchMaintenanceAlerts = async () => {
    try {
      const data = await assetAPI.getUpcomingMaintenances(30);
      setMaintenanceAlerts(data || []);
    } catch (err) {
      console.error('Erro ao buscar manutenções:', err);
    }
  };

  const fetchWarrantyAlerts = async () => {
    try {
      const data = await assetAPI.getExpiringWarranties(90);
      setWarrantyAlerts(data || []);
    } catch (err) {
      console.error('Erro ao buscar garantias:', err);
    }
  };

  const addAsset = async () => {
    if (!newAsset.nome || !newAsset.numero_tag || !newAsset.id_categoria || !newAsset.id_localizacao) {
      alert('Por favor, preencha os campos obrigatórios: Nome, Tag, Categoria e Localização');
      return;
    }

    try {
      // Validação de tag única
      const tagValidation = await assetAPI.validateAssetTag(newAsset.numero_tag);
      if (!tagValidation.available) {
        alert('Esta tag já está em uso. Por favor, escolha outra.');
        return;
      }

      const assetToSend = {
        ...newAsset,
        custo_aquisicao: newAsset.custo_aquisicao ? parseFloat(newAsset.custo_aquisicao) : 0,
        valor_atual: newAsset.valor_atual ? parseFloat(newAsset.valor_atual) : 
                   (newAsset.custo_aquisicao ? parseFloat(newAsset.custo_aquisicao) : 0),
        valor_residual: newAsset.valor_residual ? parseFloat(newAsset.valor_residual) : 0,
        vida_util_anos: newAsset.vida_util_anos ? parseInt(newAsset.vida_util_anos) : null,
        id_fornecedor: newAsset.id_fornecedor || null
      };

      const createdAsset = await assetAPI.createAsset(assetToSend);
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

      // Atualizar dados
      await Promise.all([
        fetchDashboardData(),
        fetchStatistics(),
        fetchAlerts()
      ]);
      
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
      await assetAPI.deleteAsset(id);
      setAssets(assets.filter(asset => asset.id !== id));
      
      // Atualizar dados
      await Promise.all([
        fetchDashboardData(),
        fetchStatistics()
      ]);
      
      alert('Ativo excluído com sucesso!');
    } catch (err) {
      setError(err.message);
      alert(`Erro: ${err.message}`);
    }
  };

  const updateAssetStatus = async (id, newStatus) => {
    try {
      await assetAPI.updateAsset(id, { status_ativo: newStatus });
      
      // Atualizar localmente
      setAssets(assets.map(asset => 
        asset.id === id ? { ...asset, status_ativo: newStatus } : asset
      ));
      
      await fetchDashboardData();
      alert('Status atualizado com sucesso!');
    } catch (err) {
      setError(err.message);
      alert(`Erro: ${err.message}`);
    }
  };

  const exportAssets = async (format = 'csv') => {
    try {
      const data = await assetAPI.exportAssets(format);
      
      if (format === 'csv') {
        const blob = new Blob([data], { type: 'text/csv;charset=utf-8;' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ativos_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      } else {
        // Para JSON
        const jsonStr = JSON.stringify(data, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ativos_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      }
      
      alert(`Ativos exportados em ${format.toUpperCase()} com sucesso!`);
    } catch (err) {
      setError(err.message);
      alert(`Erro ao exportar: ${err.message}`);
    }
  };

  const getStatusBadgeClass = (status) => {
    return assetAPI.getStatusBadgeClass(status);
  };

  const getCriticalityBadgeClass = (criticality) => {
    return assetAPI.getCriticalityBadgeClass(criticality);
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
        <button 
          className={`tab-btn ${activeTab === 'alertas' ? 'active' : ''}`}
          onClick={() => setActiveTab('alertas')}
        >
          Alertas
        </button>
      </div>

      <div className="module-content">
        {activeTab === 'dashboard' && (
          <>
            {/* Dashboard Cards */}
            <div className="asset-summary">
              <div className="summary-card">
                <h3>Total de Ativos</h3>
                <p className="count">{dashboardData?.total_ativos || assets.length}</p>
              </div>
              <div className="summary-card">
                <h3>Valor Total</h3>
                <p className="value">{assetAPI.formatCurrency(dashboardData?.valor_total || 
                  assets.reduce((sum, asset) => sum + (asset.valor_atual || asset.custo_aquisicao || 0), 0))}
                </p>
              </div>
              <div className="summary-card">
                <h3>Categorias</h3>
                <p className="categories">{dashboardData?.total_categorias || categories.length}</p>
              </div>
              <div className="summary-card">
                <h3>Status Ativos</h3>
                <p className="count">
                  {assets.filter(a => a.status_ativo === 'ativo').length}
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
                    {Object.entries(
                      assets.reduce((acc, asset) => {
                        acc[asset.status_ativo] = (acc[asset.status_ativo] || 0) + 1;
                        return acc;
                      }, {})
                    ).map(([status, quantidade]) => (
                      <li key={status}>
                        <span className="stat-label">{assetAPI.formatStatus(status)}:</span>
                        <span className="stat-value">{quantidade}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="stats-card">
                  <h4>Ativos por Categoria</h4>
                  <ul className="stats-list">
                    {categories.slice(0, 5).map(category => {
                      const count = assets.filter(a => a.id_categoria === category.id).length;
                      return count > 0 ? (
                        <li key={category.id}>
                          <span className="stat-label">{category.nome}:</span>
                          <span className="stat-value">{count}</span>
                        </li>
                      ) : null;
                    })}
                  </ul>
                </div>
                <div className="stats-card">
                  <h4>Ativos por Criticidade</h4>
                  <ul className="stats-list">
                    {['baixa', 'medio', 'alta', 'critico'].map(criticality => {
                      const count = assets.filter(a => a.criticidade === criticality).length;
                      return count > 0 ? (
                        <li key={criticality}>
                          <span className="stat-label">{assetAPI.formatCriticality(criticality)}:</span>
                          <span className="stat-value">{count}</span>
                        </li>
                      ) : null;
                    })}
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
                <button onClick={() => exportAssets('csv')} className="btn btn-secondary btn-sm mr-2">
                  Exportar CSV
                </button>
                <button onClick={() => exportAssets('json')} className="btn btn-secondary btn-sm">
                  Exportar JSON
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
                        <td>
                          {categories.find(c => c.id === asset.id_categoria)?.nome || 
                           `Categoria ${asset.id_categoria}`}
                        </td>
                        <td>
                          {locations.find(l => l.id === asset.id_localizacao)?.nome || 
                           `Local ${asset.id_localizacao}`}
                        </td>
                        <td>{assetAPI.formatDate(asset.data_aquisicao)}</td>
                        <td>{assetAPI.formatCurrency(asset.valor_atual || asset.custo_aquisicao)}</td>
                        <td>
                          <span className={`status-badge ${getStatusBadgeClass(asset.status_ativo)}`}>
                            {assetAPI.formatStatus(asset.status_ativo)}
                          </span>
                        </td>
                        <td>
                          <span className={`criticidade-badge ${getCriticalityBadgeClass(asset.criticidade)}`}>
                            {assetAPI.formatCriticality(asset.criticidade)}
                          </span>
                        </td>
                        <td>
                          <div className="action-buttons">
                            <select 
                              value={asset.status_ativo}
                              onChange={(e) => updateAssetStatus(asset.id, e.target.value)}
                              className="form-control-sm status-select"
                            >
                              <option value="ativo">Ativo</option>
                              <option value="inativo">Inativo</option>
                              <option value="em_manutencao">Manutenção</option>
                              <option value="baixado">Baixado</option>
                            </select>
                            <button 
                              onClick={() => deleteAsset(asset.id)}
                              className="btn btn-danger btn-sm"
                              title="Excluir ativo"
                            >
                              Excluir
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}

        {activeTab === 'alertas' && (
          <div className="card">
            <h2>Alertas e Notificações</h2>
            
            <div className="alerts-section">
              <h3>Próximas Manutenções (30 dias)</h3>
              {maintenanceAlerts.length > 0 ? (
                <div className="table-container">
                  <table>
                    <thead>
                      <tr>
                        <th>Ativo</th>
                        <th>Tag</th>
                        <th>Última Manutenção</th>
                        <th>Próxima Manutenção</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {maintenanceAlerts.map(alert => (
                        <tr key={alert.id}>
                          <td>{alert.nome_ativo}</td>
                          <td><strong>{alert.numero_tag}</strong></td>
                          <td>{assetAPI.formatDate(alert.ultima_manutencao)}</td>
                          <td>{assetAPI.formatDate(alert.proxima_manutencao)}</td>
                          <td>
                            <span className={`status-badge ${getStatusBadgeClass(alert.status_ativo)}`}>
                              {assetAPI.formatStatus(alert.status_ativo)}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p>Nenhuma manutenção programada para os próximos 30 dias.</p>
              )}

              <h3>Garantias a Vencer (90 dias)</h3>
              {warrantyAlerts.length > 0 ? (
                <div className="table-container">
                  <table>
                    <thead>
                      <tr>
                        <th>Ativo</th>
                        <th>Tag</th>
                        <th>Fornecedor</th>
                        <th>Vencimento</th>
                        <th>Dias Restantes</th>
                      </tr>
                    </thead>
                    <tbody>
                      {warrantyAlerts.map(alert => (
                        <tr key={alert.id}>
                          <td>{alert.nome_ativo}</td>
                          <td><strong>{alert.numero_tag}</strong></td>
                          <td>{alert.fornecedor_nome || 'N/A'}</td>
                          <td>{assetAPI.formatDate(alert.data_vencimento_garantia)}</td>
                          <td>
                            <span className={`badge ${parseInt(alert.dias_restantes) < 30 ? 'badge-danger' : 'badge-warning'}`}>
                              {alert.dias_restantes} dias
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p>Nenhuma garantia vencendo nos próximos 90 dias.</p>
              )}

              <h3>Outros Alertas</h3>
              {alerts.length > 0 ? (
                <div className="table-container">
                  <table>
                    <thead>
                      <tr>
                        <th>Tipo</th>
                        <th>Mensagem</th>
                        <th>Data</th>
                        <th>Severidade</th>
                      </tr>
                    </thead>
                    <tbody>
                      {alerts.map(alert => (
                        <tr key={alert.id}>
                          <td>{alert.tipo}</td>
                          <td>{alert.mensagem}</td>
                          <td>{assetAPI.formatDateTime(alert.data_criacao)}</td>
                          <td>
                            <span className={`badge ${alert.severidade === 'alta' ? 'badge-danger' : 
                                              alert.severidade === 'media' ? 'badge-warning' : 'badge-info'}`}>
                              {alert.severidade}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p>Nenhum alerta recente.</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AssetManagement;