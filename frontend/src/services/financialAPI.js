// src/services/financialApi.js
import api from './api';

const financialApi = {
  // ========== CONTAS FINANCEIRAS ==========
  getAccounts: (params) => api.get('/financeiro/contas', { params }),
  getAccount: (id) => api.get(`/financeiro/contas/${id}`),
  createAccount: (data) => api.post('/financeiro/contas', data),
  updateAccount: (id, data) => api.put(`/financeiro/contas/${id}`, data),
  deleteAccount: (id) => api.delete(`/financeiro/contas/${id}`),

  // ========== EXTRATOS ==========
  getStatements: (params) => api.get('/financeiro/extratos', { params }),
  getStatement: (id) => api.get(`/financeiro/extratos/${id}`),
  createStatement: (data) => api.post('/financeiro/extratos', data),
  updateStatement: (id, data) => api.put(`/financeiro/extratos/${id}`, data),
  deleteStatement: (id) => api.delete(`/financeiro/extratos/${id}`),

  // ========== FLUXO DE CAIXA ==========
  getCashFlows: (params) => api.get('/financeiro/fluxo-caixa', { params }),
  getCashFlow: (id) => api.get(`/financeiro/fluxo-caixa/${id}`),
  createCashFlow: (data) => api.post('/financeiro/fluxo-caixa', data),
  updateCashFlow: (id, data) => api.put(`/financeiro/fluxo-caixa/${id}`, data),
  deleteCashFlow: (id) => api.delete(`/financeiro/fluxo-caixa/${id}`),

  // ========== CONCILIAÇÕES ==========
  getReconciliations: (params) => api.get('/financeiro/conciliacoes', { params }),
  getReconciliation: (id) => api.get(`/financeiro/conciliacoes/${id}`),
  createReconciliation: (data) => api.post('/financeiro/conciliacoes', data),
  updateReconciliation: (id, data) => api.put(`/financeiro/conciliacoes/${id}`, data),
  deleteReconciliation: (id) => api.delete(`/financeiro/conciliacoes/${id}`),

  // ========== ORÇAMENTOS ==========
  getBudgets: (params) => api.get('/financeiro/orcamentos', { params }),
  getBudget: (id) => api.get(`/financeiro/orcamentos/${id}`),
  createBudget: (data) => api.post('/financeiro/orcamentos', data),
  updateBudget: (id, data) => api.put(`/financeiro/orcamentos/${id}`, data),
  deleteBudget: (id) => api.delete(`/financeiro/orcamentos/${id}`),

  // ========== CONTABILIDADE ==========
  // Lançamentos Contábeis
  getAccountingEntries: (params) => api.get('/contabilidade/lancamentos', { params }),
  getAccountingEntry: (id) => api.get(`/contabilidade/lancamentos/${id}`),
  createAccountingEntry: (data) => api.post('/contabilidade/lancamentos', data),
  updateAccountingEntry: (id, data) => api.put(`/contabilidade/lancamentos/${id}`, data),
  deleteAccountingEntry: (id) => api.delete(`/contabilidade/lancamentos/${id}`),

  // Planos de Contas
  getChartOfAccounts: (params) => api.get('/contabilidade/planos-contas', { params }),
  getChartOfAccount: (id) => api.get(`/contabilidade/planos-contas/${id}`),
  createChartOfAccount: (data) => api.post('/contabilidade/planos-contas', data),
  updateChartOfAccount: (id, data) => api.put(`/contabilidade/planos-contas/${id}`, data),
  deleteChartOfAccount: (id) => api.delete(`/contabilidade/planos-contas/${id}`),

  // ========== FISCAL ==========
  // Impostos
  getTaxes: (params) => api.get('/fiscal/impostos', { params }),
  getTax: (id) => api.get(`/fiscal/impostos/${id}`),
  createTax: (data) => api.post('/fiscal/impostos', data),
  updateTax: (id, data) => api.put(`/fiscal/impostos/${id}`, data),
  deleteTax: (id) => api.delete(`/fiscal/impostos/${id}`),

  // Notas Fiscais
  getInvoices: (params) => api.get('/fiscal/notas-fiscais', { params }),
  getInvoice: (id) => api.get(`/fiscal/notas-fiscais/${id}`),
  createInvoice: (data) => api.post('/fiscal/notas-fiscais', data),
  updateInvoice: (id, data) => api.put(`/fiscal/notas-fiscais/${id}`, data),
  deleteInvoice: (id) => api.delete(`/fiscal/notas-fiscais/${id}`),

  // ========== RELATÓRIOS FINANCEIROS ==========
  getFinancialReport: (params) => api.get('/financeiro/relatorios', { params }),
  getCashFlowReport: (params) => api.get('/financeiro/relatorios/fluxo-caixa', { params }),
  getBudgetReport: (params) => api.get('/financeiro/relatorios/orcamento', { params }),

  // ========== DASHBOARD FINANCEIRO ==========
  getFinancialDashboard: () => api.get('/financeiro/dashboard'),
  getFinancialSummary: (params) => api.get('/financeiro/resumo', { params }),

  // ========== SAÚDE DO MÓDULO ==========
  healthCheck: () => api.get('/financeiro/health')
};

export default financialApi;