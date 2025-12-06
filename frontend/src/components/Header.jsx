import React from 'react';
import '../styles/Header.css';

const Header = ({ onLogout, onToggleSidebar }) => {
  return (
    <header className="header">
      <div className="header-left">
        <button className="sidebar-toggle" onClick={onToggleSidebar}>
          <span>☰</span>
        </button>
        <h1 className="logo">BluERP</h1>
      </div>
      <div className="header-right">
        <div className="user-info">
          <span className="welcome">Bem-vindo, Usuário</span>
          <button onClick={onLogout} className="logout-btn">
            Sair
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;