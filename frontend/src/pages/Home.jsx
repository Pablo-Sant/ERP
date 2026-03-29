import React from "react";
import { Link } from "react-router-dom";
import "../styles/Home.css";

const modules = [
  "Gestao de Materiais",
  "Financeiro e Fiscal",
  "Gestao de Ativos",
  "Recursos Humanos",
  "Vendas e Compras",
  "Business Intelligence",
];

export default function Home() {
  return (
    <div className="home">
      <nav className="home-nav">
        <div className="nav-brand">
          <h2>BluERP</h2>
        </div>
        <div className="nav-links">
          <Link className="nav-link" to="/sobre">
            Sobre
          </Link>
          <Link className="nav-link login-link" to="/login">
            Entrar
          </Link>
        </div>
      </nav>

      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">
            Gestao empresarial integrada para operações mais eficientes
          </h1>
          <p className="hero-subtitle">
            O BluERP conecta setores essenciais da empresa em uma unica
            plataforma, promovendo controle, organização e visibilidade sobre
            processos operacionais, financeiros e comerciais.
          </p>
          <div className="hero-buttons">
            <Link className="btn btn-primary" to="/login">
              Acessar o sistema
            </Link>
            <Link className="btn btn-secondary" to="/sobre">
              Conhecer o projeto
            </Link>
          </div>
        </div>
      </section>

      <section className="features-section">
        <div className="container">
          <h2 className="section-title">Módulos do BluERP</h2>
          <div className="features-grid">
            {modules.map((module) => (
              <div className="feature-card" key={module}>
                <h3 className="feature-title">{module}</h3>
                <p className="feature-description">
                  Recursos organizados para apoiar a rotina da empresa com mais
                  integração entre áreas e informações.
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
