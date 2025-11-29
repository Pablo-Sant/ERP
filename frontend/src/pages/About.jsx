import React from 'react';
import { Link } from 'react-router-dom';
import "../styles/About.css";

const About = () => {
  return (
    <div className="about-page">
      <nav className="home-nav">
        <div className="nav-brand">
          <h2>ERP System</h2>
        </div>
        <div className="nav-links">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/login" className="nav-link login-link">Login</Link>
        </div>
      </nav>

      <div className="about-container">
        <div className="about-header">
          <h1>Sobre o ERP System</h1>
          <p>Solução completa para gestão empresarial</p>
        </div>

        <div className="about-content">
          <div className="about-section">
            <h2>Nossa Missão</h2>
            <p>
              Fornecer uma plataforma de gestão integrada que simplifique os processos empresariais, 
              aumente a eficiência operacional e proporcione insights valiosos para a tomada de decisões estratégicas.
            </p>
          </div>

          <div className="about-section">
            <h2>O Sistema</h2>
            <p>
              Desenvolvido com as mais modernas tecnologias, nosso ERP oferece módulos especializados 
              para cada área da empresa, permitindo gestão unificada e em tempo real de todos os processos.
            </p>
          </div>

          <div className="features-highlight">
            <div className="feature-item">
              <h3>✅ Integração Completa</h3>
              <p>Todos os departamentos conectados em uma única plataforma</p>
            </div>
            <div className="feature-item">
              <h3>✅ Relatórios em Tempo Real</h3>
              <p>Dados atualizados instantaneamente para decisões precisas</p>
            </div>
            <div className="feature-item">
              <h3>✅ Segurança de Dados</h3>
              <p>Proteção avançada para suas informações empresariais</p>
            </div>
            <div className="feature-item">
              <h3>✅ Suporte 24/7</h3>
              <p>Assistência técnica sempre disponível</p>
            </div>
          </div>

          <div className="about-cta">
            <Link to="/login" className="btn btn-primary">Experimente Grátis</Link>
            <Link to="/" className="btn btn-secondary">Voltar para Home</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;