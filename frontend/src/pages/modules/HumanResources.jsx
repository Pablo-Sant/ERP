import React from 'react';
import EntityPanel from '../../components/EntityPanel';
import ModuleShell from '../../components/ModuleShell';
import { erpApi } from '../../services/erpApi';
import { formatCurrency, formatDate } from '../../utils/formatters';

export default function HumanResources() {
  return (
    <ModuleShell
      description="Cadastro e acompanhamento de funcoes e colaboradores para apoio a operacao de Recursos Humanos."
      title="Recursos Humanos"
    >
      <EntityPanel
        columns={[
          { key: 'id', label: 'ID' },
          { key: 'nome', label: 'Nome' },
          { key: 'descricao', label: 'Descrição' },
        ]}
        createItem={erpApi.hr.createRole}
        deleteItem={erpApi.hr.deleteRole}
        fields={[
          { name: 'nome', label: 'Nome', required: true },
          { name: 'descricao', label: 'Descrição', type: 'textarea' },
        ]}
        getItemKey={(item) => item.id}
        loadItems={erpApi.hr.listRoles}
        title="Funções"
      />

      <EntityPanel
        columns={[
          { key: 'id', label: 'ID' },
          { key: 'nome', label: 'Nome' },
          { key: 'cpf', label: 'CPF' },
          { key: 'email', label: 'E-mail' },
          { key: 'funcao_id', label: 'Função ID' },
          { key: 'data_contratacao', label: 'Contratação', render: (item) => formatDate(item.data_contratacao) },
          { key: 'salario', label: 'Salário', render: (item) => formatCurrency(item.salario) },
        ]}
        createItem={erpApi.hr.createEmployee}
        deleteItem={erpApi.hr.deleteEmployee}
        fields={[
          { name: 'nome', label: 'Nome', required: true },
          { name: 'cpf', label: 'CPF', required: true },
          { name: 'email', label: 'E-mail', type: 'email' },
          { name: 'funcao_id', label: 'Função ID', type: 'number' },
          { name: 'data_contratacao', label: 'Data de contratação', type: 'date', required: true },
          { name: 'carga_horaria', label: 'Carga horária', type: 'number', required: true },
          { name: 'data_de_nascimento', label: 'Nascimento', type: 'date' },
          { name: 'data_de_recrutamento', label: 'Data de recrutamento', type: 'date', required: true },
          { name: 'salario', label: 'Salário', type: 'number', step: '0.01', required: true },
        ]}
        getItemKey={(item) => item.id}
        loadItems={erpApi.hr.listEmployees}
        title="Colaboradores"
      />
    </ModuleShell>
  );
}
