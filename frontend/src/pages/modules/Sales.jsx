import React from 'react';
import EntityPanel from '../../components/EntityPanel';
import ModuleShell from '../../components/ModuleShell';
import { erpApi } from '../../services/erpApi';
import { formatCurrency, formatDate } from '../../utils/formatters';

export default function Sales() {
  return (
    <ModuleShell
      description="Visao comercial com gestao de clientes, vendedores, contratos e pedidos de venda."
      title="Vendas e Compras"
    >
      <EntityPanel
        columns={[
          { key: 'cliente_finalid', label: 'ID' },
          { key: 'nome', label: 'Nome' },
          { key: 'cpf_cnpj', label: 'CPF/CNPJ' },
          { key: 'email', label: 'E-mail' },
          { key: 'telefone', label: 'Telefone' },
          { key: 'cidade', label: 'Cidade' },
          { key: 'valor_compra', label: 'Valor compra', render: (item) => formatCurrency(item.valor_compra) },
        ]}
        createItem={erpApi.sales.createClient}
        deleteItem={erpApi.sales.deleteClient}
        fields={[
          { name: 'nome', label: 'Nome', required: true },
          { name: 'cpf_cnpj', label: 'CPF/CNPJ' },
          { name: 'email', label: 'E-mail', type: 'email' },
          { name: 'telefone', label: 'Telefone' },
          { name: 'endereco', label: 'Endereço' },
          { name: 'cidade', label: 'Cidade' },
        ]}
        getItemKey={(item) => item.cliente_finalid}
        loadItems={erpApi.sales.listClients}
        title="Clientes finais"
      />

      <EntityPanel
        columns={[
          { key: 'vendedorid', label: 'ID' },
          { key: 'nome', label: 'Nome' },
          { key: 'cpf_cnpj', label: 'CPF/CNPJ' },
          { key: 'email', label: 'E-mail' },
          { key: 'telefone', label: 'Telefone' },
          { key: 'status', label: 'Status' },
        ]}
        createItem={erpApi.sales.createSeller}
        deleteItem={erpApi.sales.deleteSeller}
        fields={[
          { name: 'nome', label: 'Nome', required: true },
          { name: 'cpf_cnpj', label: 'CPF/CNPJ', required: true },
          { name: 'inscricao_estadual', label: 'Inscrição estadual' },
          { name: 'email', label: 'E-mail', type: 'email' },
          { name: 'telefone', label: 'Telefone' },
          { name: 'endereco', label: 'Endereço' },
          { name: 'cidade', label: 'Cidade' },
          { name: 'estado', label: 'Estado' },
          { name: 'site', label: 'Site' },
          { name: 'status', label: 'Status' },
          { name: 'data_cadastro', label: 'Data de cadastro', type: 'date' },
        ]}
        getItemKey={(item) => item.vendedorid}
        loadItems={erpApi.sales.listSellers}
        title="Vendedores"
      />

      <EntityPanel
        columns={[
          { key: 'contratoid', label: 'ID' },
          { key: 'cliente_finalid', label: 'Cliente ID' },
          { key: 'vendedorid', label: 'Vendedor ID' },
          { key: 'data_inicio', label: 'Início', render: (item) => formatDate(item.data_inicio) },
          { key: 'vencimento', label: 'Vencimento', render: (item) => formatDate(item.vencimento) },
        ]}
        createItem={erpApi.sales.createContract}
        deleteItem={erpApi.sales.deleteContract}
        fields={[
          { name: 'cliente_finalid', label: 'Cliente ID', type: 'number', required: true },
          { name: 'vendedorid', label: 'Vendedor ID', type: 'number', required: true },
          { name: 'data_inicio', label: 'Data de início', type: 'date' },
          { name: 'vencimento', label: 'Vencimento', type: 'date' },
        ]}
        getItemKey={(item) => item.contratoid}
        loadItems={erpApi.sales.listContracts}
        title="Contratos"
      />

      <EntityPanel
        columns={[
          { key: 'pedidoid', label: 'ID' },
          { key: 'cliente_finalid', label: 'Cliente ID' },
          { key: 'vendedorid', label: 'Vendedor ID' },
          { key: 'data_prevista_entrega', label: 'Entrega', render: (item) => formatDate(item.data_prevista_entrega) },
          { key: 'hora', label: 'Hora' },
          { key: 'status', label: 'Status' },
        ]}
        createItem={erpApi.sales.createOrder}
        deleteItem={erpApi.sales.deleteOrder}
        fields={[
          { name: 'cliente_finalid', label: 'Cliente ID', type: 'number', required: true },
          { name: 'vendedorid', label: 'Vendedor ID', type: 'number', required: true },
          { name: 'data_prevista_entrega', label: 'Data prevista', type: 'date' },
          { name: 'hora', label: 'Hora', type: 'time' },
          { name: 'status', label: 'Status' },
        ]}
        getItemKey={(item) => item.pedidoid}
        loadItems={erpApi.sales.listOrders}
        title="Pedidos de venda"
      />
    </ModuleShell>
  );
}
