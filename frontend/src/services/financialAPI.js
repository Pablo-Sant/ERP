// src/services/financialApi.js
import api from './api';

const financialApi = {
  // Contas
  getAccounts: (params) => api.get('/fi/contas', { params }),
  getAccount: (id) => api.get(`/fi/contas/${id}`),
  createAccount: (data) => api.post('/fi/contas', data),
  updateAccount: (id, data) => api.put(`/fi/contas/${id}`, data),
  deleteAccount: (id) => api.delete(`/fi/contas/${id}`),

  // Transações
  getTransactions: (params) => api.get('/fi/lancamentos', { params }),
  getTransaction: (id) => api.get(`/fi/lancamentos/${id}`),
  createTransaction: (data) => api.post('/fi/lancamentos', data),
  updateTransaction: (id, data) => api.put(`/fi/lancamentos/${id}`, data),
  deleteTransaction: (id) => api.delete(`/fi/lancamentos/${id}`),

  // Dashboard
  getDashboard: () => api.get('/fi/dashboard'),
  getReports: (params) => api.get('/fi/relatorios/receitas-despesas', { params }),

  // Orçamentos
  getBudgets: (params) => api.get('/fi/orcamentos', { params }),
  createBudget: (data) => api.post('/fi/orcamentos', data),

  // Fluxo de Caixa
  getCashFlow: (params) => api.get('/fi/fluxo-caixa', { params }),
  generateCashFlow: (data) => api.post('/fi/fluxo-caixa/gerar', null, { params: data }),

  // Notas Fiscais
  getInvoices: (params) => api.get('/fi/notas-fiscais', { params }),
  createInvoice: (data) => api.post('/fi/notas-fiscais', data),

  // Saúde do módulo
  healthCheck: () => api.get('/fi/health')
};

export default financialApi;