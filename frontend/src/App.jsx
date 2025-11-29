import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './styles/App.css';

// Components
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Footer from './components/Footer';

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
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <div className="App">
        {!isAuthenticated ? (
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/sobre" element={<About />} />
            <Route path="/login" element={<Login onLogin={handleLogin} />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        ) : (
          <div className="app-layout">
            <Header 
              onLogout={handleLogout} 
              onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
            />
            <div className="main-content">
              <Sidebar 
                isOpen={sidebarOpen} 
                onClose={() => setSidebarOpen(false)}
              />
              <div className="content-area">
                <Routes>
                  <Route path="/dashboard" element={<Dashboard />} />
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