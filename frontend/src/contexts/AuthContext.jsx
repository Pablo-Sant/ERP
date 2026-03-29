import React, { createContext, useEffect, useMemo, useState } from 'react';
import api, { setUnauthorizedHandler } from '../services/api';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('authToken'));
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem('user');
    return storedUser ? JSON.parse(storedUser) : null;
  });
  const [loading, setLoading] = useState(true);

  const logout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
    delete api.defaults.headers.common.Authorization;
  };

  useEffect(() => {
    setUnauthorizedHandler(logout);
  }, []);

  useEffect(() => {
    if (token) {
      api.defaults.headers.common.Authorization = `Bearer ${token}`;
    } else {
      delete api.defaults.headers.common.Authorization;
    }
  }, [token]);

  useEffect(() => {
    async function bootstrap() {
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const response = await api.get('/usuarios/me');
        setUser(response.data);
        localStorage.setItem('user', JSON.stringify(response.data));
      } catch (error) {
        logout();
      } finally {
        setLoading(false);
      }
    }

    bootstrap();
  }, [token]);

  const login = async ({ email, password }) => {
    const body = new URLSearchParams();
    body.append('username', email);
    body.append('password', password);

    const tokenResponse = await api.post('/usuarios/login', body, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

    const nextToken = tokenResponse.data.access_token;
    localStorage.setItem('authToken', nextToken);
    setToken(nextToken);

    const meResponse = await api.get('/usuarios/me', {
      headers: { Authorization: `Bearer ${nextToken}` },
    });

    localStorage.setItem('user', JSON.stringify(meResponse.data));
    setUser(meResponse.data);
    return meResponse.data;
  };

  const value = useMemo(
    () => ({
      isAuthenticated: Boolean(token && user),
      loading,
      login,
      logout,
      token,
      user,
    }),
    [loading, token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
