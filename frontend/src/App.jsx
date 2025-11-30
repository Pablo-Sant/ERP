// src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import './styles/App.css';

// Components
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Footer from './components/Footer';
import Loading from './components/Loading'; // Usando seu componente Loading

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

function App() {
  const { isAuthenticated, user, loading, logout } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Mostra o loading enquanto verifica a autenticação
  if (loading) {
    return <Loading />;
  }

  return (
    <Router>
      <div className="App">
        {!isAuthenticated ? (
          // Rotas públicas (usuário não autenticado)
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/sobre" element={<About />} />
            <Route path="/login" element={<Login />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        ) : (
          // Layout principal (usuário autenticado)
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
                <Routes>
                  <Route path="/dashboard" element={<Dashboard user={user} />} />
                  <Route path="/ps" element={<ProjectManagement />} />
                  <Route path="/mm" element={<MaterialManagement />} />
                  <Route path="/fi" element={<Financial />} />
                  <Route path="/am" element={<AssetManagement />} />
                  <Route path="/rh" element={<HumanResources />} />
                  <Route path="/vc" element={<Sales />} />
                  <Route path="/sm" element={<Services />} />
                  <Route path="/bi" element={<BusinessIntelligence />} />
                  <Route path="*" element={<Navigate to="/dashboard" />} />
                </Routes>
              </div>
            </div>
            <Footer />
          </div>
        )}
      </div>
    </Router>
  );
}

export default App;