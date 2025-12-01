// src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import './styles/App.css';

// Components
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Footer from './components/Footer';
import Loading from './components/Loading';

// Pages
import Home from './pages/Home';
import About from './pages/About';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

// Módulos
import ProjectManagement from './pages/modules/ProjectManagement';
import MaterialManagement from './pages/modules/MaterialManagement';
import Financial from './pages/modules/Financial';
import AssetManagement from './pages/modules/AssetManagement';
import HumanResources from './pages/modules/HumanResources';
import Sales from './pages/modules/Sales';
import Services from './pages/modules/Services';
import BusinessIntelligence from './pages/modules/BusinessIntelligence';

// Componente para Layout Autenticado
const AuthenticatedLayout = ({ user, logout, children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="app-layout">
      <Header 
        user={user}
        onLogout={logout} 
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
      />
      <div className="main-content">
        <Sidebar 
          isOpen={sidebarOpen} 
          onClose={() => setSidebarOpen(false)}
          user={user}
        />
        <div className="content-area">
          {children}
        </div>
      </div>
      <Footer />
    </div>
  );
};

// Componente para Rotas Protegidas
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, user, logout, loading } = useAuth();

  if (loading) {
    return <Loading />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <AuthenticatedLayout user={user} logout={logout}>
      {children}
    </AuthenticatedLayout>
  );
};

// Componente para Rotas Públicas
const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <Loading />;
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

function App() {
  const { loading } = useAuth();

  if (loading) {
    return <Loading />;
  }

  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Rotas Públicas */}
          <Route path="/" element={<Home />} />
          <Route path="/sobre" element={<About />} />
          <Route 
            path="/login" 
            element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            } 
          />
          
          {/* Rotas Protegidas */}
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/ps" 
            element={
              <ProtectedRoute>
                <ProjectManagement />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/mm" 
            element={
              <ProtectedRoute>
                <MaterialManagement />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/fi" 
            element={
              <ProtectedRoute>
                <Financial />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/am" 
            element={
              <ProtectedRoute>
                <AssetManagement />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/rh" 
            element={
              <ProtectedRoute>
                <HumanResources />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/vc" 
            element={
              <ProtectedRoute>
                <Sales />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/sm" 
            element={
              <ProtectedRoute>
                <Services />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/bi" 
            element={
              <ProtectedRoute>
                <BusinessIntelligence />
              </ProtectedRoute>
            } 
          />
          
          {/* Fallback */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;