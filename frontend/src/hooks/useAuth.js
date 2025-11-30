// src/hooks/useAuth.js - ADICIONE ESTE USEEFFECT PARA SINCRONIZAR
import { useState, useEffect } from 'react';
import api from '../services/api';

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Sincronizar com localStorage sempre que mudar
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      setUser(JSON.parse(userData));
      setIsAuthenticated(true);
    } else {
      setUser(null);
      setIsAuthenticated(false);
    }
    setLoading(false);
  }, []); // Executa apenas uma vez na montagem

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('authToken');
      
      if (token) {
        const response = await api.get('/auth/me');
        setUser(response.data);
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error('Erro ao verificar autenticação:', error);
      logout();
    }
  };

  const login = async (credentials) => {
    try {
      setLoading(true);
      
      const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      const data = await response.json();

      if (response.ok) {
        const { access_token, user } = data;
        
        // Armazenar no localStorage
        localStorage.setItem('authToken', access_token);
        localStorage.setItem('user', JSON.stringify(user));
        
        // ATUALIZAR ESTADO - isso vai forçar o rerender
        setUser(user);
        setIsAuthenticated(true);
        
        // Configurar token no axios
        if (api.defaults.headers) {
          api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        }
        
        console.log('🔐 Login realizado - estado atualizado');
        return { success: true, user };
      } else {
        return { 
          success: false, 
          error: data.detail || 'Erro no login' 
        };
      }
    } catch (error) {
      console.error('Erro no login:', error);
      return { 
        success: false, 
        error: 'Erro de conexão com o servidor' 
      };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    setUser(null);
    setIsAuthenticated(false);
    
    if (api.defaults.headers) {
      delete api.defaults.headers.common['Authorization'];
    }
  };

  return {
    isAuthenticated,
    user,
    loading,
    login,
    logout,
    checkAuth
  };
};