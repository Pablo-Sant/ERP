import React, { useState, useEffect } from 'react';
import "../../styles/Module.css";
import "../../styles/DashboardMM.css"; // Importar apenas layout
import MaterialService from '../../services/materialService';

const MaterialManagement = () => {
  const [produtos, setProdutos] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dashboard, setDashboard] = useState(null);
  const [stockAlerts, setStockAlerts] = useState([]);

  // Estados para novo produto
  const [novoProduto, setNovoProduto] = useState({
    nome: '',
    descricao: '',
    empresa_id: '',
    categoria_id: '',
    quantidade: '',
    quantidade_minima: '',
    preco_unitario: '',
    codigo_barras: '',
    unidade_medida: 'UN',
    localizacao: '',
    status: 'ativo'
  });

  // Estados para filtros
  const [filtros, setFiltros] = useState({
    empresa_id: '',
    categoria_id: '',
    search: ''
  });

  // Carregar dados iniciais
  useEffect(() => {
    carregarDados();
  }, []);

  // Carregar dados com filtros
  useEffect(() => {
    if (!loading) {
      carregarProdutos();
    }
  }, [filtros, loading]);

  const carregarDados = async () => {
    setLoading(true);
    try {
      const [produtosData, empresasData, categoriasData, dashboardData] = await Promise.all([
        MaterialService.getProdutos(),
        MaterialService.getEmpresas(),
        MaterialService.getCategorias(),
        MaterialService.getDashboard()
      ]);

      setProdutos(produtosData || []);
      setEmpresas(empresasData || []);
      setCategorias(categoriasData || []);
      setDashboard(dashboardData);
      
      // Calcular alertas de estoque
      if (produtosData) {
        const alerts = produtosData
          .filter(p => p.quantidade <= p.quantidade_minima || p.quantidade === 0)
          .slice(0, 5) // Limitar a 5 alertas
          .map(p => ({
            id: p.id,
            title: p.quantidade === 0 ? 'Produto Esgotado' : 'Estoque Baixo',
            message: `${p.nome} - Quantidade: ${p.quantidade}`,
            type: p.quantidade === 0 ? 'critical' : 'warning',
            time: 'Recentemente'
          }));
        setStockAlerts(alerts);
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      alert('Erro ao carregar dados do sistema');
    } finally {
      setLoading(false);
    }
  };

  const carregarProdutos = async () => {
    try {
      // Preparar parâmetros
      const params = {};
      if (filtros.empresa_id) params.empresa_id = filtros.empresa_id;
      if (filtros.categoria_id) params.categoria_id = filtros.categoria_id;
      if (filtros.search) params.search = filtros.search;
      
      const produtosData = await MaterialService.getProdutos(params);
      setProdutos(produtosData);
    } catch (error) {
      console.error('Erro ao carregar produtos:', error);
    }
  };

  const adicionarProduto = async () => {
    try {
      // Validações básicas
      if (!novoProduto.nome || !novoProduto.empresa_id || !novoProduto.categoria_id) {
        alert('Preencha os campos obrigatórios: Nome, Empresa e Categoria');
        return;
      }

      const produtoData = {
        ...novoProduto,
        quantidade: parseInt(novoProduto.quantidade) || 0,
        quantidade_minima: parseInt(novoProduto.quantidade_minima) || 0,
        preco_unitario: parseFloat(novoProduto.preco_unitario) || 0
      };

      const produtoCriado = await MaterialService.createProduto(produtoData);
      
      // Atualizar lista
      setProdutos([...produtos, produtoCriado]);
      
      // Limpar formulário
      setNovoProduto({
        nome: '',
        descricao: '',
        empresa_id: '',
        categoria_id: '',
        quantidade: '',
        quantidade_minima: '',
        preco_unitario: '',
        codigo_barras: '',
        unidade_medida: 'UN',
        localizacao: '',
        status: 'ativo'
      });

      // Recarregar dados para atualizar dashboard
      carregarDados();
      
      alert('Produto adicionado com sucesso!');
    } catch (error) {
      console.error('Erro ao adicionar produto:', error);
      alert(error.response?.data?.detail || 'Erro ao adicionar produto');
    }
  };

  const excluirProduto = async (id) => {
    if (!window.confirm('Tem certeza que deseja excluir este produto?')) {
      return;
    }

    try {
      await MaterialService.deleteProduto(id);
      setProdutos(produtos.filter(produto => produto.id !== id));
      alert('Produto excluído com sucesso!');
      
      // Recarregar dados para atualizar dashboard
      carregarDados();
    } catch (error) {
      console.error('Erro ao excluir produto:', error);
      alert(error.response?.data?.detail || 'Erro ao excluir produto');
    }
  };

  const formatarData = (dataString) => {
    if (!dataString) return '';
    const data = new Date(dataString);
    return data.toLocaleDateString('pt-BR');
  };

  const formatarMoeda = (valor) => {
    if (!valor) return 'R$ 0,00';
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(valor);
  };

  const getStatusEstoque = (quantidade, quantidadeMinima) => {
    if (quantidade === 0) return 'Esgotado';
    if (quantidade <= quantidadeMinima) return 'Baixo';
    if (quantidade <= quantidadeMinima * 1.5) return 'Atenção';
    return 'Normal';
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'Normal': return 'status-normal';
      case 'Atenção': return 'status-atencao';
      case 'Baixo': return 'status-baixo';
      case 'Esgotado': return 'status-esgotado';
      default: return '';
    }
  };

  if (loading) {
    return (
      <div className="material-dashboard">
        <div className="dashboard-loading">
          <div className="loading-spinner"></div>
          <p className="text-muted">Carregando dados do sistema...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="material-dashboard">
      <div className="dashboard-container">
        
        {/* Cabeçalho */}
        <header className="dashboard-header">
          <h1>Gestão de Materiais</h1>
          <p>Controle de estoque e materiais</p>
        </header>

        {/* Cards de Resumo Dashboard */}
        {dashboard && (
          <div className="summary-cards">
            <div className="summary-card total">
              <div className="card-icon">📦</div>
              <h3>Total de Produtos</h3>
              <p className="value">{dashboard.estatisticas?.total_produtos || 0}</p>
              <div className="card-trend trend-up">
                <span style={{ marginRight: '5px' }}>📈</span> {dashboard.ultimos_produtos?.length || 0} novos
              </div>
            </div>

            <div className="summary-card empresas">
              <div className="card-icon">🚚</div>
              <h3>Empresas</h3>
              <p className="value">{dashboard.estatisticas?.total_empresas || 0}</p>
              <div className="card-trend trend-up">
                <span style={{ marginRight: '5px' }}>📈</span> Ativas
              </div>
            </div>

            <div className="summary-card categorias">
              <div className="card-icon">🗂️</div>
              <h3>Categorias</h3>
              <p className="value">{dashboard.estatisticas?.total_categorias || 0}</p>
              <div className="card-trend trend-neutral">
                <span style={{ marginRight: '5px' }}>📊</span> Organizadas
              </div>
            </div>

            <div className="summary-card armazens">
              <div className="card-icon">🏠</div>
              <h3>Armazéns</h3>
              <p className="value">{dashboard.estatisticas?.total_armazens || 0}</p>
              <div className="card-trend trend-up">
                <span style={{ marginRight: '5px' }}>📈</span> Disponíveis
              </div>
            </div>

            <div className="summary-card alerta">
              <div className="card-icon">⚠️</div>
              <h3>Com Alerta</h3>
              <p className="value">
                {produtos.filter(p => p.quantidade <= p.quantidade_minima && p.quantidade > 0).length}
              </p>
              <div className="card-trend trend-down">
                <span style={{ marginRight: '5px' }}>📉</span> Atenção
              </div>
            </div>

            <div className="summary-card esgotado">
              <div className="card-icon">❌</div>
              <h3>Esgotados</h3>
              <p className="value">
                {produtos.filter(p => p.quantidade === 0).length}
              </p>
              <div className="card-trend trend-down">
                <span style={{ marginRight: '5px' }}>📉</span> Urgente
              </div>
            </div>
          </div>
        )}

        {/* Cards de Ação Rápida */}
        <div className="quick-actions">
          <div className="action-card" onClick={() => document.querySelector('.form-grid')?.scrollIntoView({ behavior: 'smooth' })}>
            <div className="action-icon">➕</div>
            <h3>Novo Produto</h3>
            <p>Cadastre um novo produto no sistema</p>
          </div>

          <div className="action-card" onClick={carregarDados}>
            <div className="action-icon">🔄</div>
            <h3>Atualizar Dados</h3>
            <p>Atualize todas as informações do sistema</p>
          </div>

          <div className="action-card" onClick={() => window.print()}>
            <div className="action-icon">📊</div>
            <h3>Gerar Relatório</h3>
            <p>Exporte relatórios do estoque</p>
          </div>

          <div className="action-card" onClick={() => alert('Funcionalidade em desenvolvimento')}>
            <div className="action-icon">🔔</div>
            <h3>Alertas</h3>
            <p>Configure notificações de estoque</p>
          </div>
        </div>

        {/* Seção Principal de Conteúdo */}
        <div className="module-content">
          
          {/* Filtros */}
          <div className="chart-card">
            <h2><span style={{ marginRight: '10px' }}>🔍</span> Filtros de Busca</h2>
            <div className="form-grid" style={{ marginTop: '20px' }}>
              <div className="form-group">
                <label><span style={{ marginRight: '5px' }}>🔎</span> Buscar Produto</label>
                <input
                  type="text"
                  value={filtros.search}
                  onChange={(e) => setFiltros({...filtros, search: e.target.value})}
                  placeholder="Digite nome ou descrição..."
                  className="form-control"
                />
              </div>
              <div className="form-group">
                <label>🏢 Empresa</label>
                <select
                  value={filtros.empresa_id}
                  onChange={(e) => setFiltros({...filtros, empresa_id: e.target.value})}
                  className="form-control"
                >
                  <option value="">Todas as empresas</option>
                  {empresas.map(empresa => (
                    <option key={empresa.id} value={empresa.id}>
                      {empresa.nome}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>🗂️ Categoria</label>
                <select
                  value={filtros.categoria_id}
                  onChange={(e) => setFiltros({...filtros, categoria_id: e.target.value})}
                  className="form-control"
                >
                  <option value="">Todas as categorias</option>
                  {categorias.map(categoria => (
                    <option key={categoria.id} value={categoria.id}>
                      {categoria.nome}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <button 
                  onClick={() => setFiltros({ empresa_id: '', categoria_id: '', search: '' })}
                  className="btn btn-secondary"
                  style={{ marginTop: '25px' }}
                >
                  <span style={{ marginRight: '5px' }}>🗑️</span> Limpar Filtros
                </button>
              </div>
            </div>
          </div>

          {/* Alertas de Estoque */}
          {stockAlerts.length > 0 && (
            <div className="alerts-section">
              <div className="alerts-header">
                <h2><span style={{ marginRight: '10px' }}>🚨</span> Alertas de Estoque</h2>
                <span className="alert-badge">{stockAlerts.length}</span>
              </div>
              
              {stockAlerts.map(alert => (
                <div key={alert.id} className={`alert-item ${alert.type}`}>
                  <div className="alert-icon">
                    {alert.type === 'critical' ? '❌' : '⚠️'}
                  </div>
                  <div className="alert-content">
                    <h4 className="alert-title">{alert.title}</h4>
                    <p className="alert-message">{alert.message}</p>
                    <div className="alert-time">{alert.time}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Formulário de Novo Produto */}
          <div className="chart-card">
            <h2><span style={{ marginRight: '10px' }}>➕</span> Cadastrar Novo Produto</h2>
            <div className="form-grid" style={{ marginTop: '20px' }}>
              <div className="form-group">
                <label>📝 Nome do Produto *</label>
                <input
                  type="text"
                  value={novoProduto.nome}
                  onChange={(e) => setNovoProduto({...novoProduto, nome: e.target.value})}
                  placeholder="Nome do produto"
                  className="form-control"
                  required
                />
              </div>
              
              <div className="form-group">
                <label>🏢 Empresa *</label>
                <select
                  value={novoProduto.empresa_id}
                  onChange={(e) => setNovoProduto({...novoProduto, empresa_id: e.target.value})}
                  className="form-control"
                  required
                >
                  <option value="">Selecione uma empresa</option>
                  {empresas.map(empresa => (
                    <option key={empresa.id} value={empresa.id}>
                      {empresa.nome}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>🗂️ Categoria *</label>
                <select
                  value={novoProduto.categoria_id}
                  onChange={(e) => setNovoProduto({...novoProduto, categoria_id: e.target.value})}
                  className="form-control"
                  required
                >
                  <option value="">Selecione uma categoria</option>
                  {categorias.map(categoria => (
                    <option key={categoria.id} value={categoria.id}>
                      {categoria.nome}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>📦 Quantidade</label>
                <input
                  type="number"
                  value={novoProduto.quantidade}
                  onChange={(e) => setNovoProduto({...novoProduto, quantidade: e.target.value})}
                  placeholder="0"
                  min="0"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>⚠️ Estoque Mínimo</label>
                <input
                  type="number"
                  value={novoProduto.quantidade_minima}
                  onChange={(e) => setNovoProduto({...novoProduto, quantidade_minima: e.target.value})}
                  placeholder="0"
                  min="0"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>💰 Preço Unitário (R$)</label>
                <input
                  type="number"
                  step="0.01"
                  value={novoProduto.preco_unitario}
                  onChange={(e) => setNovoProduto({...novoProduto, preco_unitario: e.target.value})}
                  placeholder="0,00"
                  min="0"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>📏 Unidade de Medida</label>
                <select
                  value={novoProduto.unidade_medida}
                  onChange={(e) => setNovoProduto({...novoProduto, unidade_medida: e.target.value})}
                  className="form-control"
                >
                  <option value="UN">Unidade (UN)</option>
                  <option value="KG">Quilograma (KG)</option>
                  <option value="M">Metro (M)</option>
                  <option value="LT">Litro (LT)</option>
                  <option value="CX">Caixa (CX)</option>
                </select>
              </div>

              <div className="form-group">
                <label>📋 Código de Barras</label>
                <input
                  type="text"
                  value={novoProduto.codigo_barras}
                  onChange={(e) => setNovoProduto({...novoProduto, codigo_barras: e.target.value})}
                  placeholder="Opcional"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>📍 Localização</label>
                <input
                  type="text"
                  value={novoProduto.localizacao}
                  onChange={(e) => setNovoProduto({...novoProduto, localizacao: e.target.value})}
                  placeholder="Opcional"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>📄 Descrição</label>
                <textarea
                  value={novoProduto.descricao}
                  onChange={(e) => setNovoProduto({...novoProduto, descricao: e.target.value})}
                  placeholder="Descrição detalhada do produto"
                  rows="3"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>📊 Status</label>
                <select
                  value={novoProduto.status}
                  onChange={(e) => setNovoProduto({...novoProduto, status: e.target.value})}
                  className="form-control"
                >
                  <option value="ativo">✅ Ativo</option>
                  <option value="inativo">⏸️ Inativo</option>
                </select>
              </div>

              <div className="form-group full-width">
                <button onClick={adicionarProduto} className="btn btn-primary" style={{ padding: '12px 30px' }}>
                  <span style={{ marginRight: '8px' }}>➕</span> Adicionar Produto
                </button>
                <button 
                  onClick={() => setNovoProduto({
                    nome: '',
                    descricao: '',
                    empresa_id: '',
                    categoria_id: '',
                    quantidade: '',
                    quantidade_minima: '',
                    preco_unitario: '',
                    codigo_barras: '',
                    unidade_medida: 'UN',
                    localizacao: '',
                    status: 'ativo'
                  })}
                  className="btn btn-secondary"
                  style={{ marginLeft: '10px', padding: '12px 30px' }}
                >
                  <span style={{ marginRight: '8px' }}>🗑️</span> Limpar Formulário
                </button>
              </div>
            </div>
          </div>

          {/* Lista de Produtos */}
          <div className="recent-products">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '25px' }}>
              <h2><span style={{ marginRight: '10px' }}>📦</span> Inventário ({produtos.length} produtos)</h2>
              <button onClick={carregarProdutos} className="btn btn-sm btn-secondary">
                <span style={{ marginRight: '5px' }}>🔄</span> Atualizar
              </button>
            </div>
            
            {produtos.length === 0 ? (
              <div className="empty-state">
                <div style={{ fontSize: '48px', marginBottom: '20px' }}>📦</div>
                <h3>Nenhum produto encontrado</h3>
                <p>Adicione produtos ou ajuste os filtros</p>
              </div>
            ) : (
              <div className="table-container">
                <table className="products-table">
                  <thead>
                    <tr>
                      <th>Produto</th>
                      <th>Empresa</th>
                      <th>Categoria</th>
                      <th>Quantidade</th>
                      <th>Mínimo</th>
                      <th>Preço</th>
                      <th>Status</th>
                      <th>Criado em</th>
                      <th>Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {produtos.map(produto => {
                      const statusEstoque = getStatusEstoque(
                        produto.quantidade || 0,
                        produto.quantidade_minima || 0
                      );
                      
                      const empresa = empresas.find(e => e.id === produto.empresa_id);
                      const categoria = categorias.find(c => c.id === produto.categoria_id);

                      return (
                        <tr key={produto.id}>
                          <td>
                            <strong>{produto.nome}</strong>
                            {produto.codigo_barras && (
                              <div className="text-small text-muted">
                                📋 Cód: {produto.codigo_barras}
                              </div>
                            )}
                            {produto.descricao && (
                              <div className="text-small text-muted" style={{ marginTop: '5px' }}>
                                📄 {produto.descricao.substring(0, 50)}...
                              </div>
                            )}
                          </td>
                          <td>{empresa?.nome || '-'}</td>
                          <td>{categoria?.nome || '-'}</td>
                          <td>
                            <strong>{produto.quantidade || 0}</strong> {produto.unidade_medida || 'UN'}
                          </td>
                          <td>{produto.quantidade_minima || 0}</td>
                          <td>
                            <span className="text-success" style={{ fontWeight: '600' }}>
                              {formatarMoeda(produto.preco_unitario)}
                            </span>
                          </td>
                          <td>
                            <span className={`product-status ${getStatusClass(statusEstoque)}`}>
                              {statusEstoque}
                            </span>
                          </td>
                          <td>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                              📅 {formatarData(produto.data_criacao)}
                            </div>
                          </td>
                          <td>
                            <button 
                              onClick={() => excluirProduto(produto.id)}
                              className="btn btn-danger btn-sm"
                              style={{ display: 'flex', alignItems: 'center', gap: '5px' }}
                            >
                              <span>🗑️</span> Excluir
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Estatísticas do Estoque */}
          <div className="chart-card">
            <h2><span style={{ marginRight: '10px' }}>📊</span> Estatísticas do Estoque</h2>
            <div className="stats-row" style={{ marginTop: '20px' }}>
              <div className="stat-item" style={{ textAlign: 'center', padding: '20px', background: '#f8f9fa', borderRadius: '10px' }}>
                <h3 style={{ fontSize: '1rem', color: '#666', marginBottom: '10px' }}>⚠️ Produtos com Estoque Baixo</h3>
                <p style={{ fontSize: '2.5rem', fontWeight: '700', color: '#FF9800', margin: '0' }}>
                  {produtos.filter(p => p.quantidade <= p.quantidade_minima && p.quantidade > 0).length}
                </p>
              </div>
              <div className="stat-item" style={{ textAlign: 'center', padding: '20px', background: '#f8f9fa', borderRadius: '10px' }}>
                <h3 style={{ fontSize: '1rem', color: '#666', marginBottom: '10px' }}>❌ Produtos Esgotados</h3>
                <p style={{ fontSize: '2.5rem', fontWeight: '700', color: '#F44336', margin: '0' }}>
                  {produtos.filter(p => p.quantidade === 0).length}
                </p>
              </div>
              <div className="stat-item" style={{ textAlign: 'center', padding: '20px', background: '#f8f9fa', borderRadius: '10px' }}>
                <h3 style={{ fontSize: '1rem', color: '#666', marginBottom: '10px' }}>💰 Valor Total Estoque</h3>
                <p style={{ fontSize: '1.8rem', fontWeight: '700', color: '#4CAF50', margin: '0' }}>
                  {formatarMoeda(
                    produtos.reduce((total, p) => 
                      total + ((p.quantidade || 0) * (p.preco_unitario || 0)), 0
                  ))}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer do Dashboard */}
        <footer className="dashboard-footer">
          <div className="last-update">
            📅 Última atualização: {new Date().toLocaleString('pt-BR')}
          </div>
          <div>
            <button onClick={carregarDados} className="refresh-button">
              <span style={{ marginRight: '5px' }}>🔄</span> Atualizar Sistema
            </button>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default MaterialManagement;