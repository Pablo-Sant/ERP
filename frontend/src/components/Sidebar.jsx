import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/Sidebar.css';

const modules = [
  { path: '/dashboard', name: 'Dashboard' },
  { path: '/mm', name: 'Materiais' },
  { path: '/fi', name: 'Financeiro' },
  { path: '/am', name: 'Ativos' },
  { path: '/rh', name: 'Recursos Humanos' },
  { path: '/vc', name: 'Vendas' },
  { path: '/bi', name: 'Business Intelligence' },
];

export default function Sidebar({ isOpen, onClose }) {
  const location = useLocation();

  return (
    <>
      {isOpen ? <div className="sidebar-overlay" onClick={onClose} /> : null}
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h3>Módulos</h3>
          <button className="close-sidebar" onClick={onClose} type="button">
            ×
          </button>
        </div>
        <ul className="sidebar-menu">
          {modules.map((module) => (
            <li className={location.pathname === module.path ? 'active' : ''} key={module.path}>
              <Link onClick={onClose} to={module.path}>
                <span className="text">{module.name}</span>
              </Link>
            </li>
          ))}
        </ul>
      </aside>
    </>
  );
}
