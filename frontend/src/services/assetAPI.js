// src/services/assetAPI.js
import api from './api';
import { handleApiError } from './api';

const assetAPI = {
  // ========== ATIVOS ==========
  getAssets: async (params = {}) => {
    try {
      const response = await api.get('/ativos/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createAsset: async (assetData) => {
    try {
      const response = await api.post('/ativos/', assetData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getAsset: async (id) => {
    try {
      const response = await api.get(`/ativos/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateAsset: async (id, assetData) => {
    try {
      const response = await api.put(`/ativos/${id}`, assetData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteAsset: async (id) => {
    try {
      await api.delete(`/ativos/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== CATEGORIAS DE ATIVOS ==========
  getCategories: async (params = {}) => {
    try {
      const response = await api.get('/ativos/categorias/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createCategory: async (categoryData) => {
    try {
      const response = await api.post('/ativos/categorias/', categoryData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getCategory: async (id) => {
    try {
      const response = await api.get(`/ativos/categorias/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateCategory: async (id, categoryData) => {
    try {
      const response = await api.put(`/ativos/categorias/${id}`, categoryData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteCategory: async (id) => {
    try {
      await api.delete(`/ativos/categorias/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== LOCALIZAÇÕES ==========
  getLocations: async (params = {}) => {
    try {
      const response = await api.get('/ativos/localizacoes/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createLocation: async (locationData) => {
    try {
      const response = await api.post('/ativos/localizacoes/', locationData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getLocation: async (id) => {
    try {
      const response = await api.get(`/ativos/localizacoes/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateLocation: async (id, locationData) => {
    try {
      const response = await api.put(`/ativos/localizacoes/${id}`, locationData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteLocation: async (id) => {
    try {
      await api.delete(`/ativos/localizacoes/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== DOCUMENTOS DE ATIVOS ==========
  getAssetDocuments: async (params = {}) => {
    try {
      const response = await api.get('/ativos/documentos/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createAssetDocument: async (documentData) => {
    try {
      const response = await api.post('/ativos/documentos/', documentData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getAssetDocument: async (id) => {
    try {
      const response = await api.get(`/ativos/documentos/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateAssetDocument: async (id, documentData) => {
    try {
      const response = await api.put(`/ativos/documentos/${id}`, documentData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteAssetDocument: async (id) => {
    try {
      await api.delete(`/ativos/documentos/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== MÉTRICAS DE ATIVOS ==========
  getAssetMetrics: async (params = {}) => {
    try {
      const response = await api.get('/ativos/metricas/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createAssetMetric: async (metricData) => {
    try {
      const response = await api.post('/ativos/metricas/', metricData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getAssetMetric: async (id) => {
    try {
      const response = await api.get(`/ativos/metricas/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateAssetMetric: async (id, metricData) => {
    try {
      const response = await api.put(`/ativos/metricas/${id}`, metricData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteAssetMetric: async (id) => {
    try {
      await api.delete(`/ativos/metricas/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== MOVIMENTAÇÕES DE ATIVOS ==========
  getAssetMovements: async (params = {}) => {
    try {
      const response = await api.get('/ativos/movimentacoes/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createAssetMovement: async (movementData) => {
    try {
      const response = await api.post('/ativos/movimentacoes/', movementData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getAssetMovement: async (id) => {
    try {
      const response = await api.get(`/ativos/movimentacoes/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateAssetMovement: async (id, movementData) => {
    try {
      const response = await api.put(`/ativos/movimentacoes/${id}`, movementData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  deleteAssetMovement: async (id) => {
    try {
      await api.delete(`/ativos/movimentacoes/${id}`);
      return true;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== DASHBOARD E RELATÓRIOS ==========
  getAssetDashboard: async (params = {}) => {
    try {
      const response = await api.get('/ativos/dashboard/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getAssetSummary: async (params = {}) => {
    try {
      const response = await api.get('/ativos/summary/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getAssetsByStatus: async (params = {}) => {
    try {
      const response = await api.get('/ativos/analytics/status/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getAssetsByCategory: async (params = {}) => {
    try {
      const response = await api.get('/ativos/analytics/category/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getAssetsByCriticality: async (params = {}) => {
    try {
      const response = await api.get('/ativos/analytics/criticality/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getAssetDepreciation: async (params = {}) => {
    try {
      const response = await api.get('/ativos/analytics/depreciation/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getAssetMaintenanceHistory: async (assetId, params = {}) => {
    try {
      const response = await api.get(`/ativos/${assetId}/maintenance-history/`, { params });
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

  formatStatus: (status) => {
    const statusMap = {
      'ativo': 'Ativo',
      'inativo': 'Inativo',
      'em_manutencao': 'Em Manutenção',
      'baixado': 'Baixado',
      'planejado': 'Planejado',
      'descartado': 'Descartado',
      'perdido': 'Perdido',
      'em_transporte': 'Em Transporte',
      'reservado': 'Reservado',
      'emprestado': 'Emprestado'
    };
    return statusMap[status] || status;
  },

  formatCriticality: (criticality) => {
    const criticalityMap = {
      'baixa': 'Baixa',
      'medio': 'Média',
      'alta': 'Alta',
      'critico': 'Crítico'
    };
    return criticalityMap[criticality] || criticality;
  },

  getStatusBadgeClass: (status) => {
    const classMap = {
      'ativo': 'status-ativo',
      'inativo': 'status-inativo',
      'em_manutencao': 'status-manutencao',
      'baixado': 'status-baixado',
      'planejado': 'status-planejado',
      'descartado': 'status-descartado',
      'perdido': 'status-perdido',
      'em_transporte': 'status-transporte',
      'reservado': 'status-reservado',
      'emprestado': 'status-emprestado'
    };
    return classMap[status] || 'status-ativo';
  },

  getCriticalityBadgeClass: (criticality) => {
    const classMap = {
      'baixa': 'criticidade-baixa',
      'medio': 'criticidade-medio',
      'alta': 'criticidade-alta',
      'critico': 'criticidade-critico'
    };
    return classMap[criticality] || 'criticidade-medio';
  },

  calculateDepreciation: (acquisitionCost, acquisitionDate, usefulLifeYears, residualValue = 0) => {
    if (!acquisitionCost || !acquisitionDate || !usefulLifeYears) return 0;
    
    const acquisition = new Date(acquisitionDate);
    const now = new Date();
    const monthsDiff = (now.getFullYear() - acquisition.getFullYear()) * 12 + 
                      (now.getMonth() - acquisition.getMonth());
    
    if (monthsDiff <= 0) return 0;
    
    const depreciationPerMonth = (acquisitionCost - residualValue) / (usefulLifeYears * 12);
    const depreciatedValue = depreciationPerMonth * Math.min(monthsDiff, usefulLifeYears * 12);
    
    return Math.max(0, depreciatedValue);
  },

  calculateCurrentValue: (acquisitionCost, acquisitionDate, usefulLifeYears, residualValue = 0) => {
    if (!acquisitionCost || !acquisitionDate || !usefulLifeYears) return acquisitionCost || 0;
    
    const depreciation = this.calculateDepreciation(
      acquisitionCost, 
      acquisitionDate, 
      usefulLifeYears, 
      residualValue
    );
    
    return Math.max(residualValue, acquisitionCost - depreciation);
  },

  // ========== EXPORTAÇÃO ==========
  exportAssets: async (format = 'csv', filters = {}) => {
    try {
      const response = await api.get('/ativos/export/', {
        params: { format, ...filters },
        responseType: format === 'csv' ? 'blob' : 'json',
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  exportAssetReport: async (reportType, params = {}) => {
    try {
      const response = await api.get(`/ativos/reports/${reportType}/`, {
        params: params,
        responseType: 'blob',
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== PESQUISA AVANÇADA ==========
  searchAssets: async (searchParams) => {
    try {
      const response = await api.post('/ativos/search/', searchParams);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  advancedFilter: async (filters) => {
    try {
      const response = await api.post('/ativos/filter/', filters);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== IMPORTAÇÃO ==========
  importAssets: async (file, mapping = {}) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('mapping', JSON.stringify(mapping));
      
      const response = await api.post('/ativos/import/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== BULK OPERATIONS ==========
  bulkUpdateAssets: async (updates) => {
    try {
      const response = await api.put('/ativos/bulk-update/', updates);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  bulkDeleteAssets: async (ids) => {
    try {
      const response = await api.delete('/ativos/bulk-delete/', {
        data: { ids }
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== AUDIT TRAIL ==========
  getAssetAuditTrail: async (assetId, params = {}) => {
    try {
      const response = await api.get(`/ativos/${assetId}/audit-trail/`, { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== VALIDAÇÕES ==========
  validateAssetTag: async (tag, excludeId = null) => {
    try {
      const response = await api.get('/ativos/validate/tag/', {
        params: { tag, exclude_id: excludeId }
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  validateSerialNumber: async (serialNumber, excludeId = null) => {
    try {
      const response = await api.get('/ativos/validate/serial/', {
        params: { serial_number: serialNumber, exclude_id: excludeId }
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== NOTIFICAÇÕES E ALERTAS ==========
  getAssetAlerts: async (params = {}) => {
    try {
      const response = await api.get('/ativos/alerts/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getUpcomingMaintenances: async (days = 30) => {
    try {
      const response = await api.get('/ativos/maintenance/upcoming/', {
        params: { days }
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getExpiringWarranties: async (days = 90) => {
    try {
      const response = await api.get('/ativos/warranty/expiring/', {
        params: { days }
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ========== ESTATÍSTICAS ==========
  getAssetStatistics: async (params = {}) => {
    try {
      const response = await api.get('/ativos/statistics/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getAssetValueTrend: async (params = {}) => {
    try {
      const response = await api.get('/ativos/statistics/value-trend/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getAssetAcquisitionTrend: async (params = {}) => {
    try {
      const response = await api.get('/ativos/statistics/acquisition-trend/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  }
};

export default assetAPI;