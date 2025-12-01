import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/Sidebar.css';

const Sidebar = ({ isOpen, onClose }) => {
  const location = useLocation();
  
  const modules = [
    { path: '/dashboard', name: 'Dashboard', icon: '📊' },
    { path: '/ps', name: 'Gestão de Projetos', icon: '📋' },
    { path: '/mm', name: 'Gestão de Materiais', icon: '📦' },
    { path: '/fi', name: 'Financeiro', icon: '💰' },
    { path: '/am', name: 'Gestão de Ativos', icon: '🏢' },
    { path: '/rh', name: 'Recursos Humanos', icon: '👥' },
    { path: '/vc', name: 'Vendas', icon: '🛒' },
    { path: '/sm', name: 'Serviços', icon: '🔧' },
    { path: '/bi', name: 'Business Intelligence', icon: '📈' }
  ];

  return (
    <>
      {isOpen && <div className="sidebar-overlay" onClick={onClose}></div>}
      <nav className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h3>Módulos ERP</h3>
          <button className="close-sidebar" onClick={onClose}>×</button>
        </div>
        <ul className="sidebar-menu">
          {modules.map(module => (
            <li key={module.path} className={location.pathname === module.path ? 'active' : ''}>
              <Link to={module.path} onClick={onClose}>
                <span className="icon">{module.icon}</span>
                <span className="text">{module.name}</span>
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </>
  );
};

export default Sidebar;