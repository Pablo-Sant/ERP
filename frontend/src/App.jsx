import React, { useState } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import './styles/App.css';
import { AuthProvider } from './contexts/AuthContext';
import { useAuth } from './hooks/useAuth';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Footer from './components/Footer';
import Loading from './components/Loading';
import Home from './pages/Home';
import About from './pages/About';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AssetManagement from './pages/modules/AssetManagement';
import BusinessIntelligence from './pages/modules/BusinessIntelligence';
import Financial from './pages/modules/Financial';
import HumanResources from './pages/modules/HumanResources';
import MaterialManagement from './pages/modules/MaterialManagement';
import Sales from './pages/modules/Sales';

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <Loading />;
  if (!isAuthenticated) return <Navigate replace to="/login" />;
  return children;
}

function PublicRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <Loading />;
  if (isAuthenticated) return <Navigate replace to="/dashboard" />;
  return children;
}

function AuthenticatedLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout } = useAuth();

  return (
    <div className="app-layout">
      <Header
        onLogout={logout}
        onToggleSidebar={() => setSidebarOpen((current) => !current)}
        user={user}
      />
      <div className="main-content">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        <main className="content-area">{children}</main>
      </div>
      <Footer />
    </div>
  );
}

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Home />} path="/" />
        <Route element={<About />} path="/sobre" />
        <Route
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
          path="/login"
        />
        <Route
          element={
            <ProtectedRoute>
              <AuthenticatedLayout>
                <Dashboard />
              </AuthenticatedLayout>
            </ProtectedRoute>
          }
          path="/dashboard"
        />
        <Route
          element={
            <ProtectedRoute>
              <AuthenticatedLayout>
                <MaterialManagement />
              </AuthenticatedLayout>
            </ProtectedRoute>
          }
          path="/mm"
        />
        <Route
          element={
            <ProtectedRoute>
              <AuthenticatedLayout>
                <Financial />
              </AuthenticatedLayout>
            </ProtectedRoute>
          }
          path="/fi"
        />
        <Route
          element={
            <ProtectedRoute>
              <AuthenticatedLayout>
                <AssetManagement />
              </AuthenticatedLayout>
            </ProtectedRoute>
          }
          path="/am"
        />
        <Route
          element={
            <ProtectedRoute>
              <AuthenticatedLayout>
                <HumanResources />
              </AuthenticatedLayout>
            </ProtectedRoute>
          }
          path="/rh"
        />
        <Route
          element={
            <ProtectedRoute>
              <AuthenticatedLayout>
                <Sales />
              </AuthenticatedLayout>
            </ProtectedRoute>
          }
          path="/vc"
        />
        <Route
          element={
            <ProtectedRoute>
              <AuthenticatedLayout>
                <BusinessIntelligence />
              </AuthenticatedLayout>
            </ProtectedRoute>
          }
          path="/bi"
        />
        <Route element={<Navigate replace to="/dashboard" />} path="*" />
      </Routes>
    </BrowserRouter>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}
