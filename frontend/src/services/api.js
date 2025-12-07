// src/services/api.js
import axios from 'axios';

// No Vite usamos import.meta.env em vez de process.env
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token às requisições
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratar erros de autenticação
api.interceptors.response.use(
  (response) => {
    // Você pode adicionar lógica para processar todas as respostas aqui
    return response;
  },
  (error) => {
    if (error.response) {
      // Erro da API
      if (error.response.status === 401) {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
      
      // Log de erros em desenvolvimento
      if (import.meta.env.DEV) {
        console.error('API Error:', {
          status: error.response.status,
          data: error.response.data,
          url: error.config.url,
          method: error.config.method,
        });
      }
    } else if (error.request) {
      // Erro de rede ou timeout
      console.error('Network Error:', error.message);
    } else {
      // Erro na configuração da requisição
      console.error('Request Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// Helper para tratamento de erros
export const handleApiError = (error) => {
  if (error.response) {
    return {
      message: error.response.data?.detail || 
               error.response.data?.message || 
               'Erro na requisição',
      status: error.response.status,
      data: error.response.data,
    };
  } else if (error.request) {
    return {
      message: 'Erro de conexão com o servidor',
      status: 0,
    };
  } else {
    return {
      message: error.message || 'Erro desconhecido',
      status: null,
    };
  }
};

export default api;