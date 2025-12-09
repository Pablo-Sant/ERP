// services/rhService.js
import api from './api';
import { handleApiError } from './api';

export const rhService = {
  // ========== COLABORADORES ==========
  async getColaboradores(filtros = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filtros.funcao_id) params.append('funcao_id', filtros.funcao_id);
      if (filtros.ativo !== undefined) params.append('ativo', filtros.ativo);
      if (filtros.search) params.append('search', filtros.search);
      if (filtros.skip) params.append('skip', filtros.skip);
      if (filtros.limit) params.append('limit', filtros.limit || 50);
      
      
      const response = await api.get(`/rh/colaboradores?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar colaboradores:', error);
      throw handleApiError(error);
    }
  },

  async getColaborador(id) {
    try {
      const response = await api.get(`/rh/colaboradores/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Erro ao buscar colaborador ${id}:`, error);
      throw handleApiError(error);
    }
  },

  async createColaborador(colaborador) {
    try {
      const response = await api.post('/rh/colaboradores', colaborador);
      return response.data;
    } catch (error) {
      console.error('Erro ao criar colaborador:', error);
      throw handleApiError(error);
    }
  },

  async updateColaborador(id, colaborador) {
    try {
      const response = await api.put(`/rh/colaboradores/${id}`, colaborador);
      return response.data;
    } catch (error) {
      console.error(`Erro ao atualizar colaborador ${id}:`, error);
      throw handleApiError(error);
    }
  },

  async deleteColaborador(id) {
    try {
      await api.delete(`/rh/colaboradores/${id}`);
    } catch (error) {
      console.error(`Erro ao excluir colaborador ${id}:`, error);
      throw handleApiError(error);
    }
  },

  // ========== FUNÇÕES ==========
  async getFuncoes(filtros = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filtros.search) params.append('search', filtros.search);
      if (filtros.skip) params.append('skip', filtros.skip);
      if (filtros.limit) params.append('limit', filtros.limit || 100);
      
      const response = await api.get(`/rh/funcoes?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar funções:', error);
      throw handleApiError(error);
    }
  },

  // ========== FOLHA DE PAGAMENTO ==========
  async getFolhasPagamento(filtros = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filtros.colaborador_id) params.append('colaborador_id', filtros.colaborador_id);
      if (filtros.mes) params.append('mes', filtros.mes);
      if (filtros.ano) params.append('ano', filtros.ano);
      if (filtros.skip) params.append('skip', filtros.skip);
      if (filtros.limit) params.append('limit', filtros.limit || 100);
      
      const response = await api.get(`/rh/folha-pagamento?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar folhas de pagamento:', error);
      throw handleApiError(error);
    }
  },

  // ========== RECRUTAMENTO ==========
  async getRecrutamentos(filtros = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filtros.colaborador_id) params.append('colaborador_id', filtros.colaborador_id);
      if (filtros.status) params.append('status', filtros.status);
      if (filtros.data_inicio) params.append('data_inicio', filtros.data_inicio);
      if (filtros.data_fim) params.append('data_fim', filtros.data_fim);
      if (filtros.skip) params.append('skip', filtros.skip);
      if (filtros.limit) params.append('limit', filtros.limit || 100);
      
      const response = await api.get(`/rh/recrutamento?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar recrutamentos:', error);
      throw handleApiError(error);
    }
  },

  // ========== AVALIAÇÃO DE DESEMPENHO ==========
  async getAvaliacoes(filtros = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filtros.colaborador_id) params.append('colaborador_id', filtros.colaborador_id);
      if (filtros.nota_minima) params.append('nota_minima', filtros.nota_minima);
      if (filtros.data_inicio) params.append('data_inicio', filtros.data_inicio);
      if (filtros.data_fim) params.append('data_fim', filtros.data_fim);
      if (filtros.skip) params.append('skip', filtros.skip);
      if (filtros.limit) params.append('limit', filtros.limit || 100);
      
      const response = await api.get(`/rh/avaliacoes-desempenho?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar avaliações:', error);
      throw handleApiError(error);
    }
  },

  // ========== BENEFÍCIOS ==========
  async getBeneficios(filtros = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filtros.search) params.append('search', filtros.search);
      if (filtros.skip) params.append('skip', filtros.skip);
      if (filtros.limit) params.append('limit', filtros.limit || 100);
      
      const response = await api.get(`/rh/beneficios?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar benefícios:', error);
      throw handleApiError(error);
    }
  },

  // ========== BENEFÍCIOS DE COLABORADORES ==========
  async getColaboradorBeneficios(filtros = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filtros.colaborador_id) params.append('colaborador_id', filtros.colaborador_id);
      if (filtros.beneficio_id) params.append('beneficio_id', filtros.beneficio_id);
      if (filtros.skip) params.append('skip', filtros.skip);
      if (filtros.limit) params.append('limit', filtros.limit || 100);
    
      const response = await api.get(`/rh/colaboradores-beneficios?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar benefícios de colaboradores:', error);
      throw handleApiError(error);
    }
  },

  // ========== DASHBOARD ==========
  async getDashboard() {
    try {
      const response = await api.get('/rh/dashboard');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar dashboard:', error);
      
      throw handleApiError(error);
    }
  },

  // ========== RELATÓRIOS ==========
  async getRelatorioFolhaPagamento(ano, mes) {
    try {
      const response = await api.get(`/rh/relatorios/folha-pagamento/${ano}/${mes}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar relatório de folha de pagamento:', error);
      throw handleApiError(error);
    }
  },

  async getRelatorioColaboradoresPorFuncao() {
    try {
      const response = await api.get('/rh/relatorios/colaboradores-por-funcao');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar relatório de colaboradores por função:', error);
      throw handleApiError(error);
    }
  },

  // ========== HEALTH CHECK ==========
  async checkHealth() {
    try {
      const response = await api.get('/rh/health');
      return response.data;
    } catch (error) {
      console.error('Erro ao verificar saúde da API RH:', error);
      throw handleApiError(error);
    }
  }
};


