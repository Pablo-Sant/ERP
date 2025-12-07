import React, { useState, useEffect } from 'react';
import "../../styles/Module.css";
import { rhService } from '../../services/rhService';

const HumanResources = () => {
  const [employees, setEmployees] = useState([]);
  const [funcoes, setFuncoes] = useState([]);
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [newEmployee, setNewEmployee] = useState({
    nome: '',
    cpf: '',
    email: '',
    telefone: '',
    data_nascimento: '',
    endereco: '',
    data_contratacao: '',
    salario: '',
    funcao_id: '',
    ativo: 1
  });

  // Carregar dados iniciais
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Verificar se API está acessível
      try {
        const health = await rhService.checkHealth();
        console.log('API RH Health:', health);
      } catch (healthError) {
        console.warn('API RH pode não estar disponível:', healthError);
      }
      
      // Carregar funções primeiro
      const funcoesData = await rhService.getFuncoes({ limit: 20 });
      console.log('Funções carregadas:', funcoesData);
      setFuncoes(funcoesData);
      
      // Carregar colaboradores
      const colaboradores = await rhService.getColaboradores({ limit: 50 });
      console.log('Colaboradores carregados:', colaboradores);
      setEmployees(colaboradores);
      
      // Carregar dashboard
      try {
        const dashboard = await rhService.getDashboard();
        console.log('Dashboard carregado:', dashboard);
        setDashboardData(dashboard);
      } catch (dashboardError) {
        console.warn('Dashboard não disponível:', dashboardError);
        // Não falha se apenas o dashboard não carregar
      }
      
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
      
      // Dados de fallback para desenvolvimento
      if (import.meta.env.DEV) {
        setError('API não disponível. Usando dados de demonstração.');
        
        // Dados mockados
        setFuncoes([
          { id: 1, nome: 'Desenvolvedor' },
          { id: 2, nome: 'Analista Financeiro' },
          { id: 3, nome: 'Vendedor' },
          { id: 4, nome: 'Gerente' },
          { id: 5, nome: 'Analista de RH' }
        ]);
        
        setEmployees([
          {
            id: 1,
            nome: 'João Silva',
            cpf: '123.456.789-00',
            email: 'joao@empresa.com',
            telefone: '(11) 99999-9999',
            data_nascimento: '1990-05-15',
            endereco: 'Rua A, 123',
            data_contratacao: '2022-03-15',
            salario: 8000.00,
            funcao_id: 1,
            funcao_rel: { id: 1, nome: 'Desenvolvedor' },
            ativo: 1
          },
          {
            id: 2,
            nome: 'Maria Santos',
            cpf: '987.654.321-00',
            email: 'maria@empresa.com',
            telefone: '(11) 98888-8888',
            data_nascimento: '1988-08-22',
            endereco: 'Av. B, 456',
            data_contratacao: '2021-08-20',
            salario: 6000.00,
            funcao_id: 2,
            funcao_rel: { id: 2, nome: 'Analista Financeiro' },
            ativo: 1
          },
          {
            id: 3,
            nome: 'Pedro Oliveira',
            cpf: '456.789.123-00',
            email: 'pedro@empresa.com',
            telefone: '(11) 97777-7777',
            data_nascimento: '1995-01-30',
            endereco: 'Rua C, 789',
            data_contratacao: '2023-01-10',
            salario: 5000.00,
            funcao_id: 3,
            funcao_rel: { id: 3, nome: 'Vendedor' },
            ativo: 1
          }
        ]);
        
        setDashboardData({
          status: "ativo",
          modulo: "Recursos Humanos (RH)",
          estatisticas: {
            total_colaboradores: 3,
            colaboradores_ativos: 3,
            colaboradores_inativos: 0,
            total_funcoes: 5,
            total_folhas_pagamento: 36,
            total_beneficios: 5,
            total_avaliacoes: 9,
            media_avaliacoes: 8.2,
            folha_pagamento_ultimo_mes: 19000.00
          },
          distribuicao_funcoes: [
            { funcao: "Desenvolvedor", quantidade: 1, media_salario: 8000.00 },
            { funcao: "Analista Financeiro", quantidade: 1, media_salario: 6000.00 },
            { funcao: "Vendedor", quantidade: 1, media_salario: 5000.00 }
          ],
          ultimas_contratacoes: [
            {
              id: 3,
              nome: "Pedro Oliveira",
              funcao: "Vendedor",
              data_contratacao: "2023-01-10",
              salario: 5000.00
            },
            {
              id: 1,
              nome: "João Silva",
              funcao: "Desenvolvedor",
              data_contratacao: "2022-03-15",
              salario: 8000.00
            },
            {
              id: 2,
              nome: "Maria Santos",
              funcao: "Analista Financeiro",
              data_contratacao: "2021-08-20",
              salario: 6000.00
            }
          ]
        });
      } else {
        setError('Erro ao carregar dados. Verifique sua conexão e tente novamente.');
      }
    } finally {
      setLoading(false);
    }
  };

  const addEmployee = async () => {
    if (!newEmployee.nome || !newEmployee.funcao_id) {
      alert('Nome e função são obrigatórios!');
      return;
    }

    try {
      const employeeData = {
        ...newEmployee,
        salario: parseFloat(newEmployee.salario) || 0,
        data_contratacao: newEmployee.data_contratacao || new Date().toISOString().split('T')[0]
      };

      const createdEmployee = await rhService.createColaborador(employeeData);
      
      // Adicionar função_rel para exibição imediata
      const funcao = funcoes.find(f => f.id === parseInt(newEmployee.funcao_id));
      if (funcao) {
        createdEmployee.funcao_rel = funcao;
      }
      
      // Atualizar lista local
      setEmployees([...employees, createdEmployee]);
      
      // Limpar formulário
      setNewEmployee({
        nome: '',
        cpf: '',
        email: '',
        telefone: '',
        data_nascimento: '',
        endereco: '',
        data_contratacao: '',
        salario: '',
        funcao_id: '',
        ativo: 1
      });
      
      // Recarregar dashboard
      try {
        const dashboard = await rhService.getDashboard();
        setDashboardData(dashboard);
      } catch (dashboardError) {
        console.warn('Não foi possível atualizar o dashboard:', dashboardError);
      }
      
      alert('Colaborador adicionado com sucesso!');
    } catch (err) {
      console.error('Erro ao adicionar colaborador:', err);
      alert(`Erro ao adicionar colaborador: ${err.message || err.detail || 'Erro desconhecido'}`);
    }
  };

  const deleteEmployee = async (id) => {
    if (!window.confirm('Tem certeza que deseja excluir este colaborador?')) {
      return;
    }

    try {
      // Tenta excluir via API primeiro
      if (!import.meta.env.DEV || confirm('Deseja excluir do servidor também?')) {
        await rhService.deleteColaborador(id);
      }
      
      // Atualizar lista local
      setEmployees(employees.filter(employee => employee.id !== id));
      
      // Recarregar dashboard se API estiver disponível
      if (!import.meta.env.DEV) {
        try {
          const dashboard = await rhService.getDashboard();
          setDashboardData(dashboard);
        } catch (dashboardError) {
          console.warn('Não foi possível atualizar o dashboard:', dashboardError);
        }
      }
      
      alert('Colaborador excluído com sucesso!');
    } catch (err) {
      console.error('Erro ao excluir colaborador:', err);
      
      // Em desenvolvimento, permite excluir apenas localmente
      if (import.meta.env.DEV && confirm('API não disponível. Excluir apenas localmente?')) {
        setEmployees(employees.filter(employee => employee.id !== id));
        alert('Colaborador excluído localmente!');
      } else {
        alert(`Erro ao excluir colaborador: ${err.message || err.detail || 'Erro desconhecido'}`);
      }
    }
  };

  const toggleEmployeeStatus = async (employee) => {
    const novoStatus = employee.ativo ? 0 : 1;
    
    try {
      if (!import.meta.env.DEV) {
        await rhService.updateColaborador(employee.id, { ativo: novoStatus });
      }
      
      // Atualizar lista local
      setEmployees(employees.map(emp => 
        emp.id === employee.id ? { ...emp, ativo: novoStatus } : emp
      ));
      
      // Recarregar dashboard se API estiver disponível
      if (!import.meta.env.DEV) {
        try {
          const dashboard = await rhService.getDashboard();
          setDashboardData(dashboard);
        } catch (dashboardError) {
          console.warn('Não foi possível atualizar o dashboard:', dashboardError);
        }
      }
      
      alert(`Status do colaborador atualizado para ${novoStatus ? 'Ativo' : 'Inativo'}!`);
    } catch (err) {
      console.error('Erro ao atualizar status:', err);
      
      // Em desenvolvimento, permite atualizar localmente
      if (import.meta.env.DEV && confirm('API não disponível. Atualizar apenas localmente?')) {
        setEmployees(employees.map(emp => 
          emp.id === employee.id ? { ...emp, ativo: novoStatus } : emp
        ));
        alert('Status atualizado localmente!');
      } else {
        alert(`Erro ao atualizar status: ${err.message || err.detail || 'Erro desconhecido'}`);
      }
    }
  };

  const getStatusText = (ativo) => {
    return ativo ? 'Ativo' : 'Inativo';
  };

  const getStatusClass = (ativo) => {
    return ativo ? 'ativo' : 'inativo';
  };

  const getDepartamento = (funcaoNome) => {
    if (!funcaoNome) return 'Outros';
    
    const departamentos = {
      'Desenvolvedor': 'TI',
      'Analista de TI': 'TI',
      'Analista Financeiro': 'Financeiro',
      'Contador': 'Financeiro',
      'Vendedor': 'Comercial',
      'Gerente Comercial': 'Comercial',
      'Gerente': 'Administrativo',
      'Analista de RH': 'RH',
      'Analista de Marketing': 'Marketing'
    };
    
    return departamentos[funcaoNome] || 'Outros';
  };

  const formatCurrency = (value) => {
    if (!value && value !== 0) return 'R$ 0,00';
    return `R$ ${parseFloat(value).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    try {
      return new Date(dateString).toLocaleDateString('pt-BR');
    } catch {
      return dateString;
    }
  };

  if (loading) {
    return (
      <div className="module">
        <div className="module-header">
          <h1>Recursos Humanos</h1>
          <p>Gestão de colaboradores</p>
        </div>
        <div className="module-content">
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Carregando dados do RH...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="module">
      <div className="module-header">
        <h1>Recursos Humanos</h1>
        <p>Gestão de colaboradores</p>
      </div>

      {error && (
        <div className="alert alert-warning">
          <strong>Atenção:</strong> {error}
          <button onClick={loadInitialData} className="btn btn-sm btn-primary ml-2">
            Tentar Novamente
          </button>
        </div>
      )}

      <div className="module-content">
        {/* Resumo do Dashboard */}
        <div className="hr-summary">
          {dashboardData ? (
            <>
              <div className="summary-card">
                <h3>Total de Colaboradores</h3>
                <p className="count">{dashboardData.estatisticas.total_colaboradores}</p>
              </div>
              <div className="summary-card">
                <h3>Ativos</h3>
                <p className="active">{dashboardData.estatisticas.colaboradores_ativos}</p>
              </div>
              <div className="summary-card">
                <h3>Inativos</h3>
                <p className="inactive">{dashboardData.estatisticas.colaboradores_inativos}</p>
              </div>
              <div className="summary-card">
                <h3>Folha Último Mês</h3>
                <p className="departments">{formatCurrency(dashboardData.estatisticas.folha_pagamento_ultimo_mes)}</p>
              </div>
            </>
          ) : (
            <>
              <div className="summary-card">
                <h3>Total de Colaboradores</h3>
                <p className="count">{employees.length}</p>
              </div>
              <div className="summary-card">
                <h3>Ativos</h3>
                <p className="active">{employees.filter(e => e.ativo).length}</p>
              </div>
              <div className="summary-card">
                <h3>Inativos</h3>
                <p className="inactive">{employees.filter(e => !e.ativo).length}</p>
              </div>
              <div className="summary-card">
                <h3>Funções</h3>
                <p className="departments">{funcoes.length}</p>
              </div>
            </>
          )}
        </div>

        {/* Formulário para novo colaborador */}
        <div className="card">
          <h2>Novo Colaborador</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Nome Completo *</label>
              <input
                type="text"
                value={newEmployee.nome}
                onChange={(e) => setNewEmployee({...newEmployee, nome: e.target.value})}
                placeholder="Nome do colaborador"
                required
              />
            </div>
            
            <div className="form-group">
              <label>CPF</label>
              <input
                type="text"
                value={newEmployee.cpf}
                onChange={(e) => setNewEmployee({...newEmployee, cpf: e.target.value})}
                placeholder="000.000.000-00"
              />
            </div>
            
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={newEmployee.email}
                onChange={(e) => setNewEmployee({...newEmployee, email: e.target.value})}
                placeholder="email@empresa.com"
              />
            </div>
            
            <div className="form-group">
              <label>Telefone</label>
              <input
                type="text"
                value={newEmployee.telefone}
                onChange={(e) => setNewEmployee({...newEmployee, telefone: e.target.value})}
                placeholder="(11) 99999-9999"
              />
            </div>
            
            <div className="form-group">
              <label>Data de Nascimento</label>
              <input
                type="date"
                value={newEmployee.data_nascimento}
                onChange={(e) => setNewEmployee({...newEmployee, data_nascimento: e.target.value})}
              />
            </div>
            
            <div className="form-group">
              <label>Data de Contratação</label>
              <input
                type="date"
                value={newEmployee.data_contratacao}
                onChange={(e) => setNewEmployee({...newEmployee, data_contratacao: e.target.value})}
              />
            </div>
            
            <div className="form-group">
              <label>Salário</label>
              <input
                type="number"
                step="0.01"
                value={newEmployee.salario}
                onChange={(e) => setNewEmployee({...newEmployee, salario: e.target.value})}
                placeholder="0.00"
              />
            </div>
            
            <div className="form-group">
              <label>Função *</label>
              <select
                value={newEmployee.funcao_id}
                onChange={(e) => setNewEmployee({...newEmployee, funcao_id: e.target.value})}
                required
              >
                <option value="">Selecione uma função...</option>
                {funcoes.map(funcao => (
                  <option key={funcao.id} value={funcao.id}>
                    {funcao.nome}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label>Endereço</label>
              <input
                type="text"
                value={newEmployee.endereco}
                onChange={(e) => setNewEmployee({...newEmployee, endereco: e.target.value})}
                placeholder="Endereço completo"
              />
            </div>
            
            <div className="form-group">
              <label>Status</label>
              <select
                value={newEmployee.ativo}
                onChange={(e) => setNewEmployee({...newEmployee, ativo: parseInt(e.target.value)})}
              >
                <option value="1">Ativo</option>
                <option value="0">Inativo</option>
              </select>
            </div>
            
            <div className="form-group">
              <button onClick={addEmployee} className="btn btn-primary">
                Adicionar Colaborador
              </button>
              <button 
                onClick={() => setNewEmployee({
                  nome: '',
                  cpf: '',
                  email: '',
                  telefone: '',
                  data_nascimento: '',
                  endereco: '',
                  data_contratacao: '',
                  salario: '',
                  funcao_id: '',
                  ativo: 1
                })}
                className="btn btn-secondary ml-2"
              >
                Limpar
              </button>
            </div>
          </div>
        </div>

        {/* Lista de colaboradores */}
        <div className="card">
          <h2>Colaboradores ({employees.length})</h2>
          {employees.length === 0 ? (
            <div className="no-data">
              <p>Nenhum colaborador cadastrado. Adicione o primeiro acima.</p>
            </div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Função</th>
                    <th>Departamento</th>
                    <th>Email</th>
                    <th>Telefone</th>
                    <th>Contratação</th>
                    <th>Salário</th>
                    <th>Status</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {employees.map(employee => (
                    <tr key={employee.id}>
                      <td><strong>{employee.nome}</strong></td>
                      <td>{employee.funcao_rel?.nome || 'Sem função'}</td>
                      <td>
                        <span className={`dept-badge dept-${getDepartamento(employee.funcao_rel?.nome).toLowerCase().replace(/\s+/g, '-')}`}>
                          {getDepartamento(employee.funcao_rel?.nome)}
                        </span>
                      </td>
                      <td>{employee.email || '-'}</td>
                      <td>{employee.telefone || '-'}</td>
                      <td>{formatDate(employee.data_contratacao)}</td>
                      <td>{formatCurrency(employee.salario)}</td>
                      <td>
                        <span className={`status-badge status-${getStatusClass(employee.ativo)}`}>
                          {getStatusText(employee.ativo)}
                        </span>
                      </td>
                      <td>
                        <div className="action-buttons">
                          <button 
                            onClick={() => toggleEmployeeStatus(employee)}
                            className={`btn btn-sm ${employee.ativo ? 'btn-warning' : 'btn-success'}`}
                            title={employee.ativo ? 'Inativar colaborador' : 'Ativar colaborador'}
                          >
                            {employee.ativo ? 'Inativar' : 'Ativar'}
                          </button>
                          <button 
                            onClick={() => deleteEmployee(employee.id)}
                            className="btn btn-danger btn-sm"
                            title="Excluir colaborador"
                          >
                            Excluir
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Distribuição por função */}
        <div className="card">
          <h2>Distribuição por Função</h2>
          <div className="department-stats">
            {dashboardData?.distribuicao_funcoes?.length > 0 ? (
              dashboardData.distribuicao_funcoes.map(item => (
                <div key={item.funcao} className="dept-stat">
                  <h4>{item.funcao}</h4>
                  <p>{item.quantidade} colaboradores</p>
                  {item.media_salario !== undefined && (
                    <small>Média salarial: {formatCurrency(item.media_salario)}</small>
                  )}
                </div>
              ))
            ) : (
              <div className="no-data">Nenhum dado disponível</div>
            )}
          </div>
        </div>

        {/* Últimas contratações */}
        <div className="card">
          <h2>Últimas Contratações</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Função</th>
                  <th>Data de Contratação</th>
                  <th>Salário</th>
                </tr>
              </thead>
              <tbody>
                {dashboardData?.ultimas_contratacoes?.slice(0, 5).map(contratacao => (
                  <tr key={contratacao.id}>
                    <td><strong>{contratacao.nome}</strong></td>
                    <td>{contratacao.funcao}</td>
                    <td>{formatDate(contratacao.data_contratacao)}</td>
                    <td>{formatCurrency(contratacao.salario)}</td>
                  </tr>
                ))}
                {(!dashboardData?.ultimas_contratacoes || dashboardData.ultimas_contratacoes.length === 0) && (
                  <tr>
                    <td colSpan="4" className="no-data">Nenhuma contratação recente</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HumanResources;