import React, { useState } from 'react';
import "../../styles/Module.css";

const AssetManagement = () => {
  const [assets, setAssets] = useState([
    {
      id: 1,
      tag: 'ATV-001',
      name: 'Servidor Dell R740',
      category: 'TI',
      location: 'Sala Servidores',
      purchaseDate: '2023-05-15',
      value: 'R$ 25.000',
      status: 'Ativo'
    },
    {
      id: 2,
      tag: 'ATV-002',
      name: 'Veículo Corporativo',
      category: 'Frota',
      location: 'Garagem',
      purchaseDate: '2023-08-20',
      value: 'R$ 85.000',
      status: 'Ativo'
    },
    {
      id: 3,
      tag: 'ATV-003',
      name: 'Mesa Executiva',
      category: 'Mobília',
      location: 'Sala Diretoria',
      purchaseDate: '2023-03-10',
      value: 'R$ 2.500',
      status: 'Ativo'
    }
  ]);

  const [newAsset, setNewAsset] = useState({
    tag: '',
    name: '',
    category: '',
    location: '',
    purchaseDate: '',
    value: '',
    status: 'Ativo'
  });

  const addAsset = () => {
    if (newAsset.name && newAsset.tag) {
      const asset = {
        ...newAsset,
        id: Date.now()
      };
      setAssets([...assets, asset]);
      setNewAsset({
        tag: '',
        name: '',
        category: '',
        location: '',
        purchaseDate: '',
        value: '',
        status: 'Ativo'
      });
    }
  };

  const deleteAsset = (id) => {
    setAssets(assets.filter(asset => asset.id !== id));
  };

  const totalValue = assets.reduce((sum, asset) => {
    return sum + parseFloat(asset.value.replace('R$ ', '').replace('.', '').replace(',', '.'));
  }, 0);

  return (
    <div className="module">
      <div className="module-header">
        <h1>Gestão de Ativos</h1>
        <p>Controle de patrimônio</p>
      </div>

      <div className="module-content">
        <div className="asset-summary">
          <div className="summary-card">
            <h3>Total de Ativos</h3>
            <p className="count">{assets.length}</p>
          </div>
          <div className="summary-card">
            <h3>Valor Total</h3>
            <p className="value">R$ {totalValue.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</p>
          </div>
          <div className="summary-card">
            <h3>Categorias</h3>
            <p className="categories">{new Set(assets.map(asset => asset.category)).size}</p>
          </div>
        </div>

        <div className="card">
          <h2>Novo Ativo</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Tag/Número</label>
              <input
                type="text"
                value={newAsset.tag}
                onChange={(e) => setNewAsset({...newAsset, tag: e.target.value})}
                placeholder="Número de identificação"
              />
            </div>
            <div className="form-group">
              <label>Nome do Ativo</label>
              <input
                type="text"
                value={newAsset.name}
                onChange={(e) => setNewAsset({...newAsset, name: e.target.value})}
                placeholder="Nome descritivo do ativo"
              />
            </div>
            <div className="form-group">
              <label>Categoria</label>
              <select
                value={newAsset.category}
                onChange={(e) => setNewAsset({...newAsset, category: e.target.value})}
              >
                <option value="">Selecione...</option>
                <option value="TI">TI</option>
                <option value="Mobília">Mobília</option>
                <option value="Frota">Frota</option>
                <option value="Equipamento">Equipamento</option>
                <option value="Imóvel">Imóvel</option>
              </select>
            </div>
            <div className="form-group">
              <label>Localização</label>
              <input
                type="text"
                value={newAsset.location}
                onChange={(e) => setNewAsset({...newAsset, location: e.target.value})}
                placeholder="Local onde se encontra"
              />
            </div>
            <div className="form-group">
              <label>Data Aquisição</label>
              <input
                type="date"
                value={newAsset.purchaseDate}
                onChange={(e) => setNewAsset({...newAsset, purchaseDate: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Valor</label>
              <input
                type="text"
                value={newAsset.value}
                onChange={(e) => setNewAsset({...newAsset, value: e.target.value})}
                placeholder="Valor de aquisição"
              />
            </div>
            <div className="form-group">
              <label>Status</label>
              <select
                value={newAsset.status}
                onChange={(e) => setNewAsset({...newAsset, status: e.target.value})}
              >
                <option value="Ativo">Ativo</option>
                <option value="Inativo">Inativo</option>
                <option value="Manutenção">Em Manutenção</option>
                <option value="Baixado">Baixado</option>
              </select>
            </div>
            <div className="form-group">
              <button onClick={addAsset} className="btn btn-primary">
                Adicionar Ativo
              </button>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Inventário de Ativos</h2>
          <div className="table-container">
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
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {assets.map(asset => (
                  <tr key={asset.id}>
                    <td><strong>{asset.tag}</strong></td>
                    <td>{asset.name}</td>
                    <td>{asset.category}</td>
                    <td>{asset.location}</td>
                    <td>{asset.purchaseDate}</td>
                    <td>{asset.value}</td>
                    <td>
                      <span className={`status-badge status-${asset.status.toLowerCase().replace(' ', '-')}`}>
                        {asset.status}
                      </span>
                    </td>
                    <td>
                      <button 
                        onClick={() => deleteAsset(asset.id)}
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

export default AssetManagement;