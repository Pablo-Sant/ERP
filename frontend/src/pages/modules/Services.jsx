import React, { useState } from 'react';
import "../../styles/Module.css";

const Services = () => {
  const [tickets, setTickets] = useState([
    {
      id: 1,
      number: 'TKT-001',
      client: 'Empresa ABC Ltda',
      subject: 'Problema no acesso ao sistema',
      description: 'Usuário não consegue acessar o módulo financeiro',
      priority: 'Alta',
      status: 'Aberto',
      assignedTo: 'Técnico João',
      createdAt: '2024-01-05 09:30',
      updatedAt: '2024-01-05 09:30'
    },
    {
      id: 2,
      number: 'TKT-002',
      client: 'Comércio XYZ',
      subject: 'Dúvida sobre relatório',
      description: 'Preciso de ajuda para gerar relatório de vendas',
      priority: 'Média',
      status: 'Em Andamento',
      assignedTo: 'Analista Maria',
      createdAt: '2024-01-04 14:15',
      updatedAt: '2024-01-05 10:00'
    },
    {
      id: 3,
      number: 'TKT-003',
      client: 'Indústria 123',
      subject: 'Solicitação de treinamento',
      description: 'Necessitamos de treinamento para novos usuários',
      priority: 'Baixa',
      status: 'Fechado',
      assignedTo: 'Instrutor Pedro',
      createdAt: '2024-01-03 11:00',
      updatedAt: '2024-01-04 16:30'
    }
  ]);

  const [newTicket, setNewTicket] = useState({
    client: '',
    subject: '',
    description: '',
    priority: 'Média',
    status: 'Aberto',
    assignedTo: ''
  });

  const addTicket = () => {
    if (newTicket.client && newTicket.subject) {
      const ticket = {
        ...newTicket,
        id: Date.now(),
        number: `TKT-${String(tickets.length + 1).padStart(3, '0')}`,
        createdAt: new Date().toLocaleString('pt-BR'),
        updatedAt: new Date().toLocaleString('pt-BR')
      };
      setTickets([...tickets, ticket]);
      setNewTicket({
        client: '',
        subject: '',
        description: '',
        priority: 'Média',
        status: 'Aberto',
        assignedTo: ''
      });
    }
  };

  const deleteTicket = (id) => {
    setTickets(tickets.filter(ticket => ticket.id !== id));
  };

  const updateTicketStatus = (id, newStatus) => {
    setTickets(tickets.map(ticket => 
      ticket.id === id 
        ? { ...ticket, status: newStatus, updatedAt: new Date().toLocaleString('pt-BR') }
        : ticket
    ));
  };

  return (
    <div className="module">
      <div className="module-header">
        <h1>Serviços</h1>
        <p>Atendimento ao cliente</p>
      </div>

      <div className="module-content">
        <div className="services-summary">
          <div className="summary-card">
            <h3>Tickets Abertos</h3>
            <p className="open">{tickets.filter(t => t.status === 'Aberto').length}</p>
          </div>
          <div className="summary-card">
            <h3>Em Andamento</h3>
            <p className="progress">{tickets.filter(t => t.status === 'Em Andamento').length}</p>
          </div>
          <div className="summary-card">
            <h3>Fechados</h3>
            <p className="closed">{tickets.filter(t => t.status === 'Fechado').length}</p>
          </div>
        </div>

        <div className="card">
          <h2>Novo Ticket</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Cliente</label>
              <input
                type="text"
                value={newTicket.client}
                onChange={(e) => setNewTicket({...newTicket, client: e.target.value})}
                placeholder="Nome do cliente"
              />
            </div>
            <div className="form-group">
              <label>Assunto</label>
              <input
                type="text"
                value={newTicket.subject}
                onChange={(e) => setNewTicket({...newTicket, subject: e.target.value})}
                placeholder="Assunto do ticket"
              />
            </div>
            <div className="form-group full-width">
              <label>Descrição</label>
              <textarea
                value={newTicket.description}
                onChange={(e) => setNewTicket({...newTicket, description: e.target.value})}
                placeholder="Descreva detalhadamente o problema ou solicitação"
                rows="3"
              />
            </div>
            <div className="form-group">
              <label>Prioridade</label>
              <select
                value={newTicket.priority}
                onChange={(e) => setNewTicket({...newTicket, priority: e.target.value})}
              >
                <option value="Baixa">Baixa</option>
                <option value="Média">Média</option>
                <option value="Alta">Alta</option>
                <option value="Urgente">Urgente</option>
              </select>
            </div>
            <div className="form-group">
              <label>Atribuir para</label>
              <input
                type="text"
                value={newTicket.assignedTo}
                onChange={(e) => setNewTicket({...newTicket, assignedTo: e.target.value})}
                placeholder="Nome do responsável"
              />
            </div>
            <div className="form-group">
              <label>Status</label>
              <select
                value={newTicket.status}
                onChange={(e) => setNewTicket({...newTicket, status: e.target.value})}
              >
                <option value="Aberto">Aberto</option>
                <option value="Em Andamento">Em Andamento</option>
                <option value="Fechado">Fechado</option>
              </select>
            </div>
            <div className="form-group">
              <button onClick={addTicket} className="btn btn-primary">
                Abrir Ticket
              </button>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Tickets de Serviço</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Número</th>
                  <th>Cliente</th>
                  <th>Assunto</th>
                  <th>Prioridade</th>
                  <th>Status</th>
                  <th>Responsável</th>
                  <th>Atualizado em</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {tickets.map(ticket => (
                  <tr key={ticket.id}>
                    <td><strong>{ticket.number}</strong></td>
                    <td>{ticket.client}</td>
                    <td>{ticket.subject}</td>
                    <td>
                      <span className={`priority-badge priority-${ticket.priority.toLowerCase()}`}>
                        {ticket.priority}
                      </span>
                    </td>
                    <td>
                      <select
                        value={ticket.status}
                        onChange={(e) => updateTicketStatus(ticket.id, e.target.value)}
                        className={`status-select status-${ticket.status.toLowerCase().replace(' ', '-')}`}
                      >
                        <option value="Aberto">Aberto</option>
                        <option value="Em Andamento">Em Andamento</option>
                        <option value="Fechado">Fechado</option>
                      </select>
                    </td>
                    <td>{ticket.assignedTo}</td>
                    <td>{ticket.updatedAt}</td>
                    <td>
                      <button 
                        onClick={() => deleteTicket(ticket.id)}
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
          <h2>Detalhes do Ticket</h2>
          <div className="ticket-details">
            {tickets.length > 0 && (
              <div className="ticket-detail">
                <h4>{tickets[0].number} - {tickets[0].subject}</h4>
                <p><strong>Cliente:</strong> {tickets[0].client}</p>
                <p><strong>Descrição:</strong> {tickets[0].description}</p>
                <p><strong>Prioridade:</strong> 
                  <span className={`priority-badge priority-${tickets[0].priority.toLowerCase()}`}>
                    {tickets[0].priority}
                  </span>
                </p>
                <p><strong>Responsável:</strong> {tickets[0].assignedTo}</p>
                <p><strong>Aberto em:</strong> {tickets[0].createdAt}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Services;