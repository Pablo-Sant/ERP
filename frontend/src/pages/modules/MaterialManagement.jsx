import React, { useState } from 'react';
import "../../styles/Module.css";

const MaterialManagement = () => {
  const [inventory, setInventory] = useState([
    {
      id: 1,
      name: 'Notebook Dell',
      category: 'TI',
      quantity: 15,
      minStock: 5,
      price: 'R$ 3.200',
      supplier: 'Fornecedor A'
    },
    {
      id: 2,
      name: 'Mouse Óptico',
      category: 'TI',
      quantity: 45,
      minStock: 20,
      price: 'R$ 45,90',
      supplier: 'Fornecedor B'
    },
    {
      id: 3,
      name: 'Papel A4',
      category: 'Escritório',
      quantity: 8,
      minStock: 10,
      price: 'R$ 28,50',
      supplier: 'Fornecedor C'
    }
  ]);

  const [newItem, setNewItem] = useState({
    name: '',
    category: '',
    quantity: '',
    minStock: '',
    price: '',
    supplier: ''
  });

  const addItem = () => {
    if (newItem.name && newItem.quantity) {
      const item = {
        ...newItem,
        id: Date.now()
      };
      setInventory([...inventory, item]);
      setNewItem({ 
        name: '', 
        category: '', 
        quantity: '', 
        minStock: '', 
        price: '', 
        supplier: '' 
      });
    }
  };

  const deleteItem = (id) => {
    setInventory(inventory.filter(item => item.id !== id));
  };

  const getStockStatus = (quantity, minStock) => {
    if (quantity <= minStock) return 'Baixo';
    if (quantity <= minStock * 2) return 'Atenção';
    return 'Normal';
  };

  return (
    <div className="module">
      <div className="module-header">
        <h1>Gestão de Materiais</h1>
        <p>Controle de estoque e compras</p>
      </div>

      <div className="module-content">
        <div className="card">
          <h2>Controle de Estoque</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Nome do Item</label>
              <input
                type="text"
                value={newItem.name}
                onChange={(e) => setNewItem({...newItem, name: e.target.value})}
                placeholder="Nome do produto"
              />
            </div>
            <div className="form-group">
              <label>Categoria</label>
              <input
                type="text"
                value={newItem.category}
                onChange={(e) => setNewItem({...newItem, category: e.target.value})}
                placeholder="Categoria do item"
              />
            </div>
            <div className="form-group">
              <label>Quantidade</label>
              <input
                type="number"
                value={newItem.quantity}
                onChange={(e) => setNewItem({...newItem, quantity: e.target.value})}
                placeholder="Quantidade em estoque"
              />
            </div>
            <div className="form-group">
              <label>Estoque Mínimo</label>
              <input
                type="number"
                value={newItem.minStock}
                onChange={(e) => setNewItem({...newItem, minStock: e.target.value})}
                placeholder="Estoque mínimo"
              />
            </div>
            <div className="form-group">
              <label>Preço</label>
              <input
                type="text"
                value={newItem.price}
                onChange={(e) => setNewItem({...newItem, price: e.target.value})}
                placeholder="Preço unitário"
              />
            </div>
            <div className="form-group">
              <label>Fornecedor</label>
              <input
                type="text"
                value={newItem.supplier}
                onChange={(e) => setNewItem({...newItem, supplier: e.target.value})}
                placeholder="Nome do fornecedor"
              />
            </div>
            <div className="form-group">
              <button onClick={addItem} className="btn btn-primary">
                Adicionar Item
              </button>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Inventário</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Item</th>
                  <th>Categoria</th>
                  <th>Quantidade</th>
                  <th>Estoque Mín.</th>
                  <th>Preço</th>
                  <th>Fornecedor</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {inventory.map(item => {
                  const status = getStockStatus(item.quantity, item.minStock);
                  return (
                    <tr key={item.id}>
                      <td><strong>{item.name}</strong></td>
                      <td>{item.category}</td>
                      <td>{item.quantity}</td>
                      <td>{item.minStock}</td>
                      <td>{item.price}</td>
                      <td>{item.supplier}</td>
                      <td>
                        <span className={`status-badge status-${status.toLowerCase()}`}>
                          {status}
                        </span>
                      </td>
                      <td>
                        <button 
                          onClick={() => deleteItem(item.id)}
                          className="btn btn-danger btn-sm"
                        >
                          Excluir
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <h2>Resumo do Estoque</h2>
          <div className="stats-row">
            <div className="stat-item">
              <h3>Total de Itens</h3>
              <p>{inventory.length}</p>
            </div>
            <div className="stat-item">
              <h3>Itens com Estoque Baixo</h3>
              <p className="text-danger">
                {inventory.filter(item => item.quantity <= item.minStock).length}
              </p>
            </div>
            <div className="stat-item">
              <h3>Categorias</h3>
              <p>{new Set(inventory.map(item => item.category)).size}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MaterialManagement;