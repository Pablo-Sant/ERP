import React from 'react';
import EntityPanel from '../../components/EntityPanel';
import ModuleShell from '../../components/ModuleShell';
import { erpApi } from '../../services/erpApi';
import { formatDateTime } from '../../utils/formatters';

export default function MaterialManagement() {
  return (
    <ModuleShell
      description="Cadastros e consultas para apoio ao controle de materiais, produtos, categorias e armazenagem."
      title="Gestão de Materiais"
    >
      <EntityPanel
        columns={[
          { key: 'id', label: 'ID' },
          { key: 'nome', label: 'Nome' },
          { key: 'cpf_cnpj', label: 'CPF/CNPJ' },
          { key: 'data_criacao', label: 'Criada em', render: (item) => formatDateTime(item.data_criacao) },
        ]}
        createItem={erpApi.materials.createCompany}
        deleteItem={erpApi.materials.deleteCompany}
        description="Empresas relacionadas aos registros operacionais do modulo de materiais."
        fields={[
          { name: 'nome', label: 'Nome', required: true },
          { name: 'cpf_cnpj', label: 'CPF/CNPJ' },
        ]}
        getItemKey={(item) => item.id}
        loadItems={erpApi.materials.listCompanies}
        title="Empresas"
      />

      <EntityPanel
        columns={[
          { key: 'id', label: 'ID' },
          { key: 'nome', label: 'Nome' },
          { key: 'status', label: 'Status' },
          { key: 'descricao', label: 'Descrição' },
        ]}
        createItem={erpApi.materials.createCategory}
        deleteItem={erpApi.materials.deleteCategory}
        description="Categorias para classificacao e organizacao dos itens cadastrados."
        fields={[
          { name: 'nome', label: 'Nome', required: true },
          { name: 'descricao', label: 'Descrição', type: 'textarea' },
          { name: 'categoria_pai_id', label: 'Categoria pai', type: 'number' },
          { name: 'status', label: 'Status', defaultValue: 'ativo' },
        ]}
        getItemKey={(item) => item.id}
        loadItems={erpApi.materials.listCategories}
        title="Categorias"
      />

      <EntityPanel
        columns={[
          { key: 'id', label: 'ID' },
          { key: 'empresa_id', label: 'Empresa ID' },
          { key: 'nome', label: 'Nome' },
          { key: 'endereco', label: 'Endereço' },
        ]}
        createItem={erpApi.materials.createWarehouse}
        deleteItem={erpApi.materials.deleteWarehouse}
        description="Estruturas de armazenagem vinculadas as empresas cadastradas."
        fields={[
          { name: 'empresa_id', label: 'Empresa ID', type: 'number', required: true },
          { name: 'nome', label: 'Nome', required: true },
          { name: 'endereco', label: 'Endereço' },
        ]}
        getItemKey={(item) => item.id}
        loadItems={erpApi.materials.listWarehouses}
        title="Armazéns"
      />

      <EntityPanel
        columns={[
          { key: 'id', label: 'ID' },
          { key: 'empresa_id', label: 'Empresa ID' },
          { key: 'categoria_id', label: 'Categoria ID' },
          { key: 'nome', label: 'Nome' },
          { key: 'descricao', label: 'Descrição' },
          { key: 'data_criacao', label: 'Criado em', render: (item) => formatDateTime(item.data_criacao) },
        ]}
        createItem={erpApi.materials.createProduct}
        deleteItem={erpApi.materials.deleteProduct}
        description="Produtos cadastrados para composicao do catalogo e apoio ao controle operacional."
        fields={[
          { name: 'empresa_id', label: 'Empresa ID', type: 'number', required: true },
          { name: 'categoria_id', label: 'Categoria ID', type: 'number', required: true },
          { name: 'nome', label: 'Nome', required: true },
          { name: 'descricao', label: 'Descrição', type: 'textarea' },
        ]}
        getItemKey={(item) => item.id}
        loadItems={erpApi.materials.listProducts}
        title="Produtos"
      />
    </ModuleShell>
  );
}
