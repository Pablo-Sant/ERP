// src/services/salesApi.js
import api from './api';

const salesApi = {
  // ========== CLIENTES ==========
  getClients: (params) => api.get('/vc/clientes', { params }),
  getClient: (id) => api.get(`/vc/clientes/${id}`),
  createClient: (data) => api.post('/vc/clientes', data),
  updateClient: (id, data) => api.put(`/vc/clientes/${id}`, data),
  deleteClient: (id) => api.delete(`/vc/clientes/${id}`),

  // ========== VENDEDORES ==========
  getSellers: (params) => api.get('/vc/vendedores', { params }),
  getSeller: (id) => api.get(`/vc/vendedores/${id}`),
  createSeller: (data) => api.post('/vc/vendedores', data),
  updateSeller: (id, data) => api.put(`/vc/vendedores/${id}`, data),
  deleteSeller: (id) => api.delete(`/vc/vendedores/${id}`),

  // ========== PEDIDOS/VENDAS ==========
  getSales: (params) => api.get('/vc/pedidos', { params }),
  getSale: (id) => api.get(`/vc/pedidos/${id}`),
  createSale: (data) => api.post('/vc/pedidos', data),
  updateSale: (id, data) => api.put(`/vc/pedidos/${id}`, data),
  updateSaleStatus: (id, status) => api.put(`/vc/pedidos/${id}/status`, { status }),
  deleteSale: (id) => api.delete(`/vc/pedidos/${id}`),

  // ========== CONTRATOS ==========
  getContracts: (params) => api.get('/vc/contratos', { params }),
  getContract: (id) => api.get(`/vc/contratos/${id}`),
  createContract: (data) => api.post('/vc/contratos', data),
  updateContract: (id, data) => api.put(`/vc/contratos/${id}`, data),
  deleteContract: (id) => api.delete(`/vc/contratos/${id}`),

  // ========== PROSPECTOS ==========
  getProspects: (params) => api.get('/vc/prospectos', { params }),
  getProspect: (id) => api.get(`/vc/prospectos/${id}`),
  createProspect: (data) => api.post('/vc/prospectos', data),
  updateProspect: (id, data) => api.put(`/vc/prospectos/${id}`, data),
  updateProspectPhase: (id, faseFunil) => api.put(`/vc/prospectos/${id}/fase`, { fase_funil: faseFunil }),
  deleteProspect: (id) => api.delete(`/vc/prospectos/${id}`),

  // ========== HISTÓRICO DE COMPRA ==========
  getPurchaseHistory: (params) => api.get('/vc/historicos', { params }),
  getClientPurchaseHistory: (clientId) => api.get(`/vc/clientes/${clientId}/historicos`),
  createPurchaseHistory: (data) => api.post('/vc/historicos', data),
  deletePurchaseHistory: (id) => api.delete(`/vc/historicos/${id}`),

  // ========== RELATÓRIOS ==========
  getSalesBySeller: (params) => api.get('/vc/relatorios/vendas-por-vendedor', { params }),
  getActiveClients: () => api.get('/vc/relatorios/clientes-ativos'),

  // ========== DASHBOARD ==========
  getSalesDashboard: () => api.get('/vc/dashboard'),
  getSalesSummary: (params) => api.get('/vc/resumo-vendas', { params }),

  // ========== SAÚDE DO MÓDULO ==========
  healthCheck: () => api.get('/vc/health')
};

export default salesApi;