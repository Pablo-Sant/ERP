export const MODULES = {
  PS: {
    name: 'Gestão de Projetos',
    path: '/ps',
    icon: '📋',
    description: 'Planejamento e controle de projetos'
  },
  MM: {
    name: 'Gestão de Materiais', 
    path: '/mm',
    icon: '📦',
    description: 'Controle de estoque e compras'
  },
  FI: {
    name: 'Financeiro',
    path: '/fi', 
    icon: '💰',
    description: 'Contas a pagar/receber e orçamento'
  },
  AM: {
    name: 'Gestão de Ativos',
    path: '/am',
    icon: '🏢', 
    description: 'Controle de patrimônio'
  },
  RH: {
    name: 'Recursos Humanos',
    path: '/rh',
    icon: '👥',
    description: 'Gestão de colaboradores'
  },
  VC: {
    name: 'Vendas',
    path: '/vc',
    icon: '🛒',
    description: 'Gestão comercial e CRM'
  },
  SM: {
    name: 'Serviços', 
    path: '/sm',
    icon: '🔧',
    description: 'Atendimento ao cliente'
  },
  BI: {
    name: 'Business Intelligence',
    path: '/bi',
    icon: '📈',
    description: 'Relatórios e analytics'
  }
};

export const STATUS_COLORS = {
  Ativo: '#27ae60',
  Inativo: '#e74c3c', 
  Pendente: '#f39c12',
  Concluído: '#27ae60',
  'Em Andamento': '#3498db',
  Cancelado: '#95a5a6'
};