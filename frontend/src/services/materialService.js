import api from './api';

class MaterialService {
  
  // Produtos
  async getProdutos(params = {}) {
    const response = await api.get('/materiais/produtos', { params });
    return response.data;
  }

  async getProduto(id) {
    const response = await api.get(`/materiais/produtos/${id}`);
    return response.data;
  }

  async createProduto(produto) {
    const response = await api.post('/materiais/produtos', produto);
    return response.data;
  }

  async updateProduto(id, produto) {
    const response = await api.put(`/materiais/produtos/${id}`, produto);
    return response.data;
  }

  async deleteProduto(id) {
    await api.delete(`/materiais/produtos/${id}`);
  }

  // Empresas
  async getEmpresas() {
    const response = await api.get('/materiais/empresas');
    return response.data;
  }

  async createEmpresa(empresa) {
    const response = await api.post('/materiais/empresas', empresa);
    return response.data;
  }

  // Categorias
  async getCategorias() {
    const response = await api.get('/materiais/categorias');
    return response.data;
  }

  async createCategoria(categoria) {
    const response = await api.post('/materiais/categorias', categoria);
    return response.data;
  }

  // Armazéns
  async getArmazens() {
    const response = await api.get('/materiais/armazens');
    return response.data;
  }

  // Dashboard - Nota: Não há endpoint de dashboard definido em api_router.py
  // Você precisará criar este endpoint no backend ou remover esta função
  async getDashboard() {
    const response = await api.get('/bi/dashboards');
    return response.data;
  }
  
  // Métodos adicionais que podem ser úteis:
  
  // Atualizar empresa
  async updateEmpresa(id, empresa) {
    const response = await api.put(`/materiais/empresas/${id}`, empresa);
    return response.data;
  }

  // Deletar empresa
  async deleteEmpresa(id) {
    await api.delete(`/materiais/empresas/${id}`);
  }

  // Atualizar categoria
  async updateCategoria(id, categoria) {
    const response = await api.put(`/materiais/categorias/${id}`, categoria);
    return response.data;
  }

  // Deletar categoria
  async deleteCategoria(id) {
    await api.delete(`/materiais/categorias/${id}`);
  }

  // Atualizar armazém
  async updateArmazem(id, armazem) {
    const response = await api.put(`/materiais/armazens/${id}`, armazem);
    return response.data;
  }

  // Deletar armazém
  async deleteArmazem(id) {
    await api.delete(`/materiais/armazens/${id}`);
  }
}

export default new MaterialService();