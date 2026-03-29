import React from 'react';
import '../styles/Header.css';

export default function Header({ user, onLogout, onToggleSidebar }) {
  return (
    <header className="header">
      <div className="header-left">
        <button className="sidebar-toggle" onClick={onToggleSidebar} type="button">
          Menu
        </button>
        <div>
          <h1 className="logo">BluERP</h1>
          <p className="header-subtitle">Sistema de gestao empresarial integrada</p>
        </div>
      </div>
      <div className="header-right">
        <div className="user-info">
          <span className="welcome">{user?.nome ? `Bem-vindo, ${user.nome}` : 'Acesso autenticado'}</span>
          <button className="logout-btn" onClick={onLogout} type="button">
            Sair
          </button>
        </div>
      </div>
    </header>
  );
}
