// src/services/biAPI.js
import api from './api';
import { handleApiError } from './api';

const biAPI = {
  // ========== CACHE DE DADOS ==========
  getDataCache: async (params = {}) => {
    try {
      const response = await api.get('/bi/cache/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createDataCache: async (cacheData) => {
    try {
      const response = await api.post('/bi/cache/', cacheData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getDataCacheItem: async (id) => {
    try {
      const response = await api.get(`/bi/cache/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateDataCache: async (id, cacheData) => {
    try {
      const response = await api.put(`/bi/cache/${id}`, cacheData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteDataCache: async (id) => {
    try {
      await api.delete(`/bi/cache/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== DASHBOARDS ==========
  getDashboards: async (params = {}) => {
    try {
      const response = await api.get('/bi/dashboards/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createDashboard: async (dashboardData) => {
    try {
      const response = await api.post('/bi/dashboards/', dashboardData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getDashboard: async (id) => {
    try {
      const response = await api.get(`/bi/dashboards/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateDashboard: async (id, dashboardData) => {
    try {
      const response = await api.put(`/bi/dashboards/${id}`, dashboardData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteDashboard: async (id) => {
    try {
      await api.delete(`/bi/dashboards/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== KPIs ==========
  getKPIs: async (params = {}) => {
    try {
      const response = await api.get('/bi/kpis/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createKPI: async (kpiData) => {
    try {
      const response = await api.post('/bi/kpis/', kpiData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getKPI: async (id) => {
    try {
      const response = await api.get(`/bi/kpis/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateKPI: async (id, kpiData) => {
    try {
      const response = await api.put(`/bi/kpis/${id}`, kpiData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteKPI: async (id) => {
    try {
      await api.delete(`/bi/kpis/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== MÉTRICAS ESPECIAIS ==========
  getKPIMetrics: async (params = {}) => {
    try {
      const response = await api.get('/bi/kpis/metrics/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  calculateKPI: async (kpiId, calculationParams = {}) => {
    try {
      const response = await api.post(`/bi/kpis/${kpiId}/calculate`, calculationParams);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getDashboardData: async (dashboardId, filters = {}) => {
    try {
      const response = await api.get(`/bi/dashboards/${dashboardId}/data`, { params: filters });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  refreshCache: async (cacheId) => {
    try {
      const response = await api.post(`/bi/cache/${cacheId}/refresh`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== UTILIDADES ==========
  formatPercentage: (value) => {
    if (!value && value !== 0) return '0%';
    return new Intl.NumberFormat('pt-BR', {
      style: 'percent',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value / 100);
  },

  formatNumber: (value, options = {}) => {
    if (!value && value !== 0) return '0';
    const defaultOptions = {
      minimumFractionDigits: 0,
      maximumFractionDigits: 2,
    };
    return new Intl.NumberFormat('pt-BR', { ...defaultOptions, ...options }).format(value);
  },

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

  // ========== FUNÇÕES DE ANÁLISE ==========
  getTrendAnalysis: async (params = {}) => {
    try {
      const response = await api.get('/bi/analysis/trend', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getComparativeAnalysis: async (params = {}) => {
    try {
      const response = await api.get('/bi/analysis/comparative', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getPerformanceReport: async (params = {}) => {
    try {
      const response = await api.get('/bi/reports/performance', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== EXPORTAÇÃO ==========
  exportDashboard: async (dashboardId, format = 'pdf') => {
    try {
      const response = await api.get(`/bi/dashboards/${dashboardId}/export`, {
        params: { format },
        responseType: 'blob',
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  exportKPIReport: async (kpiId, format = 'pdf') => {
    try {
      const response = await api.get(`/bi/kpis/${kpiId}/report`, {
        params: { format },
        responseType: 'blob',
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },
};

export default biAPI;