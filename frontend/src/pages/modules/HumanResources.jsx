import React, { useState } from 'react';
import "../../styles/Module.css";

const HumanResources = () => {
  const [employees, setEmployees] = useState([
    {
      id: 1,
      name: 'João Silva',
      position: 'Desenvolvedor',
      department: 'TI',
      email: 'joao@empresa.com',
      phone: '(11) 99999-9999',
      admissionDate: '2022-03-15',
      status: 'Ativo'
    },
    {
      id: 2,
      name: 'Maria Santos',
      position: 'Analista Financeiro',
      department: 'Financeiro',
      email: 'maria@empresa.com',
      phone: '(11) 98888-8888',
      admissionDate: '2021-08-20',
      status: 'Ativo'
    },
    {
      id: 3,
      name: 'Pedro Oliveira',
      position: 'Vendedor',
      department: 'Comercial',
      email: 'pedro@empresa.com',
      phone: '(11) 97777-7777',
      admissionDate: '2023-01-10',
      status: 'Ativo'
    }
  ]);

  const [newEmployee, setNewEmployee] = useState({
    name: '',
    position: '',
    department: '',
    email: '',
    phone: '',
    admissionDate: '',
    status: 'Ativo'
  });

  const addEmployee = () => {
    if (newEmployee.name && newEmployee.position) {
      const employee = {
        ...newEmployee,
        id: Date.now()
      };
      setEmployees([...employees, employee]);
      setNewEmployee({
        name: '',
        position: '',
        department: '',
        email: '',
        phone: '',
        admissionDate: '',
        status: 'Ativo'
      });
    }
  };

  const deleteEmployee = (id) => {
    setEmployees(employees.filter(employee => employee.id !== id));
  };

  return (
    <div className="module">
      <div className="module-header">
        <h1>Recursos Humanos</h1>
        <p>Gestão de colaboradores</p>
      </div>

      <div className="module-content">
        <div className="hr-summary">
          <div className="summary-card">
            <h3>Total de Colaboradores</h3>
            <p className="count">{employees.length}</p>
          </div>
          <div className="summary-card">
            <h3>Ativos</h3>
            <p className="active">{employees.filter(e => e.status === 'Ativo').length}</p>
          </div>
          <div className="summary-card">
            <h3>Departamentos</h3>
            <p className="departments">{new Set(employees.map(e => e.department)).size}</p>
          </div>
        </div>

        <div className="card">
          <h2>Novo Colaborador</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Nome Completo</label>
              <input
                type="text"
                value={newEmployee.name}
                onChange={(e) => setNewEmployee({...newEmployee, name: e.target.value})}
                placeholder="Nome do colaborador"
              />
            </div>
            <div className="form-group">
              <label>Cargo</label>
              <input
                type="text"
                value={newEmployee.position}
                onChange={(e) => setNewEmployee({...newEmployee, position: e.target.value})}
                placeholder="Cargo/função"
              />
            </div>
            <div className="form-group">
              <label>Departamento</label>
              <select
                value={newEmployee.department}
                onChange={(e) => setNewEmployee({...newEmployee, department: e.target.value})}
              >
                <option value="">Selecione...</option>
                <option value="TI">TI</option>
                <option value="Financeiro">Financeiro</option>
                <option value="Comercial">Comercial</option>
                <option value="RH">RH</option>
                <option value="Operações">Operações</option>
                <option value="Marketing">Marketing</option>
              </select>
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
                value={newEmployee.phone}
                onChange={(e) => setNewEmployee({...newEmployee, phone: e.target.value})}
                placeholder="(11) 99999-9999"
              />
            </div>
            <div className="form-group">
              <label>Data Admissão</label>
              <input
                type="date"
                value={newEmployee.admissionDate}
                onChange={(e) => setNewEmployee({...newEmployee, admissionDate: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Status</label>
              <select
                value={newEmployee.status}
                onChange={(e) => setNewEmployee({...newEmployee, status: e.target.value})}
              >
                <option value="Ativo">Ativo</option>
                <option value="Inativo">Inativo</option>
                <option value="Férias">Férias</option>
                <option value="Afastado">Afastado</option>
              </select>
            </div>
            <div className="form-group">
              <button onClick={addEmployee} className="btn btn-primary">
                Adicionar Colaborador
              </button>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Colaboradores</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Cargo</th>
                  <th>Departamento</th>
                  <th>Email</th>
                  <th>Telefone</th>
                  <th>Admissão</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {employees.map(employee => (
                  <tr key={employee.id}>
                    <td><strong>{employee.name}</strong></td>
                    <td>{employee.position}</td>
                    <td>
                      <span className={`dept-badge dept-${employee.department.toLowerCase()}`}>
                        {employee.department}
                      </span>
                    </td>
                    <td>{employee.email}</td>
                    <td>{employee.phone}</td>
                    <td>{employee.admissionDate}</td>
                    <td>
                      <span className={`status-badge status-${employee.status.toLowerCase()}`}>
                        {employee.status}
                      </span>
                    </td>
                    <td>
                      <button 
                        onClick={() => deleteEmployee(employee.id)}
                        className="btn btn-danger btn-sm"
                      >
                        Excluir
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <h2>Visão por Departamento</h2>
          <div className="department-stats">
            {Array.from(new Set(employees.map(e => e.department))).map(dept => (
              <div key={dept} className="dept-stat">
                <h4>{dept}</h4>
                <p>{employees.filter(e => e.department === dept).length} colaboradores</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HumanResources;