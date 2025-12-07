import api from './api';

class MaterialService {
  
  // Produtos
  async getProdutos(params = {}) {
    const response = await api.get('/mm/produtos', { params });
    return response.data;
  }

  async getProduto(id) {
    const response = await api.get(`/mm/produtos/${id}`);
    return response.data;
  }

  async createProduto(produto) {
    const response = await api.post('/mm/produtos', produto);
    return response.data;
  }

  async updateProduto(id, produto) {
    const response = await api.put(`/mm/produtos/${id}`, produto);
    return response.data;
  }

  async deleteProduto(id) {
    await api.delete(`/mm/produtos/${id}`);
  }

  // Empresas
  async getEmpresas() {
    const response = await api.get('/mm/empresas');
    return response.data;
  }

  async createEmpresa(empresa) {
    const response = await api.post('/mm/empresas', empresa);
    return response.data;
  }

  // Categorias
  async getCategorias() {
    const response = await api.get('/mm/categorias');
    return response.data;
  }

  async createCategoria(categoria) {
    const response = await api.post('/mm/categorias', categoria);
    return response.data;
  }

  // Armazéns
  async getArmazens() {
    const response = await api.get('/mm/armazens');
    return response.data;
  }

  // Dashboard
  async getDashboard() {
    const response = await api.get('/mm/dashboard');
    return response.data;
  }
}

export default new MaterialService();