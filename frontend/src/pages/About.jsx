import React from "react";
import { Link } from "react-router-dom";
import "../styles/About.css";

export default function About() {
  return (
    <div className="about-page">
      <nav className="home-nav">
        <div className="nav-brand">
          <h2>BluERP</h2>
        </div>
        <div className="nav-links">
          <Link className="nav-link" to="/">
            Home
          </Link>
          <Link className="nav-link login-link" to="/login">
            Login
          </Link>
        </div>
      </nav>

      <div className="about-container">
        <div className="about-header">
          <h1>Sobre o BluERP</h1>
          <p>
            Uma plataforma de gestão empresarial integrada para conectar
            processos, equipes e informações.
          </p>
        </div>

        <div className="about-content">
          <div className="about-section">
            <h2>Visão do sistema</h2>
            <p>
              O BluERP foi concebido para centralizar operações de diferentes
              áreas da empresa, oferecendo uma experiência unificada para
              consulta, registro e acompanhamento de informações.
            </p>
          </div>

          <div className="about-section">
            <h2>Áreas atendidas</h2>
            <p>
              O projeto contempla módulos voltados a Gestão de Materiais,
              Financeiro, Gestão de Ativos, Recursos Humanos, Vendas e Compras e
              Business Intelligence.
            </p>
          </div>

          <div className="about-section">
            <h2>Propósito</h2>
            <p>
              O objetivo do BluERP é apoiar controle operacional,
              rastreabilidade das informações e tomada de decisão em uma
              estrutura única de gestão empresarial.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
