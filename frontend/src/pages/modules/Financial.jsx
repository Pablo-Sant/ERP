import React from 'react';
import EntityPanel from '../../components/EntityPanel';
import ModuleShell from '../../components/ModuleShell';
import { erpApi } from '../../services/erpApi';
import { formatCurrency, formatDate } from '../../utils/formatters';

export default function Financial() {
  return (
    <ModuleShell
      description="Estrutura financeira e fiscal para acompanhamento de contas, movimentacoes, orcamentos, notas e tributos."
      title="Financeiro"
    >
      <EntityPanel
        columns={[
          { key: 'id_conta', label: 'ID' },
          { key: 'nome', label: 'Nome' },
          { key: 'tipo', label: 'Tipo' },
          { key: 'saldo_inicial', label: 'Saldo inicial', render: (item) => formatCurrency(item.saldo_inicial) },
          { key: 'data_abertura', label: 'Abertura', render: (item) => formatDate(item.data_abertura) },
          { key: 'ativo', label: 'Ativa', render: (item) => (item.ativo ? 'Sim' : 'Não') },
        ]}
        createItem={erpApi.financial.createAccount}
        deleteItem={erpApi.financial.deleteAccount}
        fields={[
          { name: 'nome', label: 'Nome', required: true },
          { name: 'tipo', label: 'Tipo', required: true },
          { name: 'saldo_inicial', label: 'Saldo inicial', type: 'number', step: '0.01', required: true },
          { name: 'data_abertura', label: 'Data de abertura', type: 'date', required: true },
          { name: 'ativo', label: 'Ativa', defaultValue: 'true', asBoolean: true },
        ]}
        getItemKey={(item) => item.id_conta}
        loadItems={erpApi.financial.listAccounts}
        title="Contas financeiras"
      />

      <EntityPanel
        columns={[
          { key: 'id_extrato', label: 'ID' },
          { key: 'id_conta', label: 'Conta ID' },
          { key: 'data_movimento', label: 'Data', render: (item) => formatDate(item.data_movimento) },
          { key: 'descricao', label: 'Descrição' },
          { key: 'valor', label: 'Valor', render: (item) => formatCurrency(item.valor) },
          { key: 'tipo', label: 'Tipo' },
          { key: 'conciliado', label: 'Conciliado', render: (item) => (item.conciliado ? 'Sim' : 'Não') },
        ]}
        createItem={erpApi.financial.createStatement}
        deleteItem={erpApi.financial.deleteStatement}
        fields={[
          { name: 'id_conta', label: 'Conta ID', type: 'number', required: true },
          { name: 'data_movimento', label: 'Data do movimento', type: 'date', required: true },
          { name: 'descricao', label: 'Descrição' },
          { name: 'valor', label: 'Valor', type: 'number', step: '0.01', required: true },
          { name: 'tipo', label: 'Tipo', required: true },
          { name: 'conciliado', label: 'Conciliado', defaultValue: 'false', asBoolean: true },
        ]}
        getItemKey={(item) => item.id_extrato}
        loadItems={erpApi.financial.listStatements}
        title="Extratos bancários"
      />

      <EntityPanel
        columns={[
          { key: 'id_fluxo', label: 'ID' },
          { key: 'data', label: 'Data', render: (item) => formatDate(item.data) },
          { key: 'saldo_inicial', label: 'Saldo inicial', render: (item) => formatCurrency(item.saldo_inicial) },
          { key: 'entradas', label: 'Entradas', render: (item) => formatCurrency(item.entradas) },
          { key: 'saidas', label: 'Saídas', render: (item) => formatCurrency(item.saidas) },
          { key: 'saldo_final', label: 'Saldo final', render: (item) => formatCurrency(item.saldo_final) },
        ]}
        createItem={erpApi.financial.createCashFlow}
        deleteItem={erpApi.financial.deleteCashFlow}
        fields={[
          { name: 'data', label: 'Data', type: 'date', required: true },
          { name: 'saldo_inicial', label: 'Saldo inicial', type: 'number', step: '0.01', required: true },
          { name: 'entradas', label: 'Entradas', type: 'number', step: '0.01', required: true },
          { name: 'saidas', label: 'Saídas', type: 'number', step: '0.01', required: true },
          { name: 'saldo_final', label: 'Saldo final', type: 'number', step: '0.01', required: true },
        ]}
        getItemKey={(item) => item.id_fluxo}
        loadItems={erpApi.financial.listCashFlows}
        title="Fluxo de caixa"
      />

      <EntityPanel
        columns={[
          { key: 'id_orcamento', label: 'ID' },
          { key: 'ano', label: 'Ano' },
          { key: 'mes', label: 'Mês' },
          { key: 'id_conta', label: 'Conta ID' },
          { key: 'valor_previsto', label: 'Previsto', render: (item) => formatCurrency(item.valor_previsto) },
          { key: 'valor_realizado', label: 'Realizado', render: (item) => formatCurrency(item.valor_realizado) },
        ]}
        createItem={erpApi.financial.createBudget}
        deleteItem={erpApi.financial.deleteBudget}
        fields={[
          { name: 'ano', label: 'Ano', type: 'number', required: true },
          { name: 'mes', label: 'Mês', type: 'number', required: true },
          { name: 'id_conta', label: 'Conta ID', type: 'number', required: true },
          { name: 'valor_previsto', label: 'Valor previsto', type: 'number', step: '0.01', required: true },
          { name: 'valor_realizado', label: 'Valor realizado', type: 'number', step: '0.01', defaultValue: 0 },
        ]}
        getItemKey={(item) => item.id_orcamento}
        loadItems={erpApi.financial.listBudgets}
        title="Orçamentos"
      />

      <EntityPanel
        columns={[
          { key: 'id_nota', label: 'ID' },
          { key: 'numero_nota', label: 'Número' },
          { key: 'tipo', label: 'Tipo' },
          { key: 'valor_total', label: 'Valor total', render: (item) => formatCurrency(item.valor_total) },
          { key: 'data_emissao', label: 'Emissão', render: (item) => formatDate(item.data_emissao) },
          { key: 'status', label: 'Status' },
        ]}
        createItem={erpApi.financial.createInvoice}
        deleteItem={erpApi.financial.deleteInvoice}
        fields={[
          { name: 'numero_nota', label: 'Número da nota', required: true },
          { name: 'tipo', label: 'Tipo', required: true },
          { name: 'valor_total', label: 'Valor total', type: 'number', step: '0.01', required: true },
          { name: 'data_emissao', label: 'Data de emissão', type: 'date', required: true },
          { name: 'chave_acesso', label: 'Chave de acesso' },
          { name: 'status', label: 'Status', defaultValue: 'ativa' },
        ]}
        getItemKey={(item) => item.id_nota}
        loadItems={erpApi.financial.listInvoices}
        title="Notas fiscais"
      />

      <EntityPanel
        columns={[
          { key: 'id_imposto', label: 'ID' },
          { key: 'id_nota', label: 'Nota ID' },
          { key: 'tipo_imposto', label: 'Tipo' },
          { key: 'base_calculo', label: 'Base', render: (item) => formatCurrency(item.base_calculo) },
          { key: 'aliquota', label: 'Alíquota' },
          { key: 'valor', label: 'Valor', render: (item) => formatCurrency(item.valor) },
        ]}
        createItem={erpApi.financial.createTax}
        deleteItem={erpApi.financial.deleteTax}
        fields={[
          { name: 'id_nota', label: 'Nota ID', type: 'number', required: true },
          { name: 'tipo_imposto', label: 'Tipo de imposto', required: true },
          { name: 'base_calculo', label: 'Base de cálculo', type: 'number', step: '0.01', required: true },
          { name: 'aliquota', label: 'Alíquota', type: 'number', step: '0.01', required: true },
          { name: 'valor', label: 'Valor', type: 'number', step: '0.01', required: true },
        ]}
        getItemKey={(item) => item.id_imposto}
        loadItems={erpApi.financial.listTaxes}
        title="Impostos"
      />
    </ModuleShell>
  );
}
