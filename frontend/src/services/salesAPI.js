// src/services/salesAPI.js
import api from './api';
import { handleApiError } from './api';

const salesAPI = {
  // ========== CLIENTES ==========
  getClients: async (params = {}) => {
    try {
      const response = await api.get('/vc/clientes/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createClient: async (clientData) => {
    try {
      const response = await api.post('/vc/clientes/', clientData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getClient: async (id) => {
    try {
      const response = await api.get(`/vc/clientes/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateClient: async (id, clientData) => {
    try {
      const response = await api.put(`/vc/clientes/${id}`, clientData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteClient: async (id) => {
    try {
      await api.delete(`/vc/clientes/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== VENDEDORES ==========
  getSellers: async (params = {}) => {
    try {
      const response = await api.get('/vc/vendedores/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createSeller: async (sellerData) => {
    try {
      const response = await api.post('/vc/vendedores/', sellerData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== PEDIDOS/VENDAS ==========
  getSales: async (params = {}) => {
    try {
      const response = await api.get('/vc/pedidos/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createSale: async (saleData) => {
    try {
      const response = await api.post('/vc/pedidos/', saleData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getSale: async (id) => {
    try {
      const response = await api.get(`/vc/pedidos/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateSaleStatus: async (id, status) => {
    try {
      const response = await api.put(`/vc/pedidos/${id}/status`, null, {
        params: { status }
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteSale: async (id) => {
    try {
      await api.delete(`/vc/pedidos/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== CONTRATOS ==========
  getContracts: async (params = {}) => {
    try {
      const response = await api.get('/vc/contratos/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createContract: async (contractData) => {
    try {
      const response = await api.post('/vc/contratos/', contractData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== HISTÓRICOS DE COMPRA ==========
  getPurchaseHistory: async (params = {}) => {
    try {
      const response = await api.get('/vc/historicos/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getClientPurchaseHistory: async (clientId) => {
    try {
      const response = await api.get(`/vc/clientes/${clientId}/historicos`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== PROSPECTOS ==========
  getProspects: async (params = {}) => {
    try {
      const response = await api.get('/vc/prospectos/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createProspect: async (prospectData) => {
    try {
      const response = await api.post('/vc/prospectos/', prospectData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateProspectPhase: async (id, phase) => {
    try {
      const response = await api.put(`/vc/prospectos/${id}/fase`, null, {
        params: { fase_funil: phase }
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== RELATÓRIOS ==========
  getSalesBySellerReport: async (params = {}) => {
    try {
      const response = await api.get('/vc/relatorios/vendas-por-vendedor', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getActiveClientsReport: async () => {
    try {
      const response = await api.get('/vc/relatorios/clientes-ativos');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== UTILIDADES ==========
  formatCurrency: (value) => {
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
    return date.toLocaleDateString('pt-BR');
  },
};

export default salesAPI;