// src/services/salesAPI.js
import api from './api';
import { handleApiError } from './api';

const salesAPI = {
  // ========== CLIENTES FINAIS ==========
  getClients: async (params = {}) => {
    try {
      const response = await api.get('/vendas-compras/clientes/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createClient: async (clientData) => {
    try {
      const response = await api.post('/vendas-compras/clientes/', clientData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getClient: async (id) => {
    try {
      const response = await api.get(`/vendas-compras/clientes/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateClient: async (id, clientData) => {
    try {
      const response = await api.put(`/vendas-compras/clientes/${id}`, clientData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteClient: async (id) => {
    try {
      await api.delete(`/vendas-compras/clientes/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== PEDIDOS DE VENDA ==========
  getSales: async (params = {}) => {
    try {
      const response = await api.get('/vendas-compras/pedidos-venda/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createSale: async (saleData) => {
    try {
      const response = await api.post('/vendas-compras/pedidos-venda/', saleData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getSale: async (id) => {
    try {
      const response = await api.get(`/vendas-compras/pedidos-venda/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateSale: async (id, saleData) => {
    try {
      const response = await api.put(`/vendas-compras/pedidos-venda/${id}`, saleData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteSale: async (id) => {
    try {
      await api.delete(`/vendas-compras/pedidos-venda/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== CONTRATOS ==========
  getContracts: async (params = {}) => {
    try {
      const response = await api.get('/vendas-compras/contratos/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createContract: async (contractData) => {
    try {
      const response = await api.post('/vendas-compras/contratos/', contractData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getContract: async (id) => {
    try {
      const response = await api.get(`/vendas-compras/contratos/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateContract: async (id, contractData) => {
    try {
      const response = await api.put(`/vendas-compras/contratos/${id}`, contractData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteContract: async (id) => {
    try {
      await api.delete(`/vendas-compras/contratos/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== HISTÓRICOS DE COMPRA ==========
  getPurchaseHistory: async (params = {}) => {
    try {
      const response = await api.get('/vendas-compras/historico-compras/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getPurchaseHistoryItem: async (id) => {
    try {
      const response = await api.get(`/vendas-compras/historico-compras/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== UTILIDADES ==========
  formatCurrency: (value) => {
    if (!value && value !== 0) return 'R$ 0,00';
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 2,
    }).format(value);
  },

  parseCurrency: (currencyString) => {
    if (!currencyString) return 0;
    const cleanString = currencyString
      .replace('R$', '')
      .replace(/\./g, '')
      .replace(',', '.')
      .trim();
    return parseFloat(cleanString) || 0;
  },

  formatDate: (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString;
    return date.toLocaleDateString('pt-BR');
  },
  
  formatDateTime: (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString;
    return date.toLocaleDateString('pt-BR') + ' ' + date.toLocaleTimeString('pt-BR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  },
};

export default salesAPI;