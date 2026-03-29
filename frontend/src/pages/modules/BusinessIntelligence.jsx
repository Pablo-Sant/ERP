import React from 'react';
import EntityPanel from '../../components/EntityPanel';
import ModuleShell from '../../components/ModuleShell';
import { erpApi } from '../../services/erpApi';
import { formatDateTime, formatJson } from '../../utils/formatters';

export default function BusinessIntelligence() {
  return (
    <ModuleShell
      description="Organizacao de dashboards, metricas e estruturas de apoio a analise de dados empresariais."
      title="Business Intelligence"
    >
      <EntityPanel
        columns={[
          { key: 'id_dashboard', label: 'ID' },
          { key: 'nome', label: 'Nome' },
          { key: 'descricao', label: 'Descrição' },
          { key: 'data_atualizacao', label: 'Atualização', render: (item) => formatDateTime(item.data_atualizacao) },
          { key: 'config_json', label: 'Configuração', render: (item) => formatJson(item.config_json) },
        ]}
        createItem={erpApi.bi.createDashboard}
        deleteItem={erpApi.bi.deleteDashboard}
        fields={[
          { name: 'nome', label: 'Nome', required: true },
          { name: 'descricao', label: 'Descrição', type: 'textarea' },
          { name: 'config_json', label: 'Config JSON', type: 'json', rows: 4, placeholder: '{"layout":"grid"}' },
          { name: 'data_atualizacao', label: 'Data de atualização', type: 'datetime-local' },
        ]}
        getItemKey={(item) => item.id_dashboard}
        loadItems={erpApi.bi.listDashboards}
        title="Dashboards"
      />

      <EntityPanel
        columns={[
          { key: 'id_metrica', label: 'ID' },
          { key: 'nome', label: 'Nome' },
          { key: 'categoria', label: 'Categoria' },
          { key: 'unidade_medida', label: 'Unidade' },
          { key: 'formula_calculo', label: 'Fórmula' },
        ]}
        createItem={erpApi.bi.createKpi}
        deleteItem={erpApi.bi.deleteKpi}
        fields={[
          { name: 'nome', label: 'Nome', required: true },
          { name: 'descricao', label: 'Descrição', type: 'textarea' },
          { name: 'formula_calculo', label: 'Fórmula de cálculo' },
          { name: 'unidade_medida', label: 'Unidade de medida' },
          { name: 'categoria', label: 'Categoria' },
        ]}
        getItemKey={(item) => item.id_metrica}
        loadItems={erpApi.bi.listKpis}
        title="KPIs"
      />

      <EntityPanel
        columns={[
          { key: 'id_cache', label: 'ID' },
          { key: 'chave_cache', label: 'Chave' },
          { key: 'data_geracao', label: 'Gerado em', render: (item) => formatDateTime(item.data_geracao) },
          { key: 'data_expiracao', label: 'Expira em', render: (item) => formatDateTime(item.data_expiracao) },
          { key: 'dados_json', label: 'Dados', render: (item) => formatJson(item.dados_json) },
        ]}
        createItem={erpApi.bi.createCache}
        deleteItem={erpApi.bi.deleteCache}
        fields={[
          { name: 'chave_cache', label: 'Chave do cache', required: true },
          { name: 'dados_json', label: 'Dados JSON', type: 'json', rows: 4, required: true, placeholder: '{"kpi":"valor"}' },
          { name: 'data_geracao', label: 'Data de geração', type: 'datetime-local' },
          { name: 'data_expiracao', label: 'Data de expiração', type: 'datetime-local' },
        ]}
        getItemKey={(item) => item.id_cache}
        loadItems={erpApi.bi.listCaches}
        title="Cache de dados"
      />
    </ModuleShell>
  );
}
