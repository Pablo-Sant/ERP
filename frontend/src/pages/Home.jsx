import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Home.css';

const Home = () => {
  const features = [
    {
      icon: '📋',
      title: 'Gestão de Projetos',
      description: 'Planejamento e controle completo de projetos'
    },
    {
      icon: '📦',
      title: 'Gestão de Materiais',
      description: 'Controle de estoque e compras integrado'
    },
    {
      icon: '💰',
      title: 'Financeiro',
      description: 'Contas a pagar/receber e orçamento'
    },
    {
      icon: '🏢',
      title: 'Gestão de Ativos',
      description: 'Controle completo do patrimônio'
    },
    {
      icon: '👥',
      title: 'Recursos Humanos',
      description: 'Gestão de colaboradores'
    },
    {
      icon: '🛒',
      title: 'Vendas',
      description: 'Gestão comercial e CRM'
    },
    {
      icon: '🔧',
      title: 'Serviços',
      description: 'Atendimento ao cliente'
    },
    {
      icon: '📈',
      title: 'Business Intelligence',
      description: 'Relatórios e analytics'
    }
  ];

  return (
    <div className="home">
      <nav className="home-nav">
        <div className="nav-brand">
          <h2>ERP System</h2>
        </div>
        <div className="nav-links">
          <Link to="/sobre" className="nav-link">Sobre</Link>
          <Link to="/login" className="nav-link login-link">Login</Link>
        </div>
      </nav>

      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">Sistema ERP Completo</h1>
          <p className="hero-subtitle">Gestão integrada para sua empresa crescer de forma organizada e eficiente</p>
          <div className="hero-buttons">
            <Link to="/sobre" className="btn btn-primary">Conheça Mais</Link>
            <Link to="/login" className="btn btn-secondary">Acessar Sistema</Link>
          </div>
        </div>
      </section>

      <section className="features-section">
        <div className="container">
          <h2 className="section-title">Módulos do Sistema</h2>
          <p className="section-subtitle">Todos os recursos que sua empresa precisa em uma única plataforma</p>
          <div className="features-grid">
            {features.map((feature, index) => (
              <div key={index} className="feature-card">
                <div className="feature-icon">{feature.icon}</div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="container">
          <h2>Pronto para transformar sua gestão?</h2>
          <p>Junte-se a centenas de empresas que já otimizaram seus processos com nosso ERP</p>
          <Link to="/login" className="btn btn-large">Começar Agora</Link>
        </div>
      </section>

      <footer className="home-footer">
        <div className="container">
          <p>&copy; 2024 ERP System. Desenvolvido para otimizar sua gestão empresarial.</p>
        </div>
      </footer>
    </div>
  );
};

export default Home;