import React from "react";
import EntityPanel from "../../components/EntityPanel";
import ModuleShell from "../../components/ModuleShell";
import { erpApi } from "../../services/erpApi";
import { formatCurrency, formatDateTime } from "../../utils/formatters";

export default function AssetManagement() {
  return (
    <ModuleShell
      description="Controle patrimonial com cadastros de categorias, localizacoes e ativos da organizacao."
      title="Gestão de Ativos"
    >
      <EntityPanel
        columns={[
          { key: "id", label: "ID" },
          { key: "codigo", label: "Código" },
          { key: "nome", label: "Nome" },
          { key: "metodo_depreciacao", label: "Método" },
          { key: "vida_util_padrao_anos", label: "Vida útil" },
          {
            key: "ativo",
            label: "Ativa",
            render: (item) => (item.ativo ? "Sim" : "Não"),
          },
        ]}
        createItem={erpApi.assets.createCategory}
        deleteItem={erpApi.assets.deleteCategory}
        fields={[
          {
            name: "id_organizacao",
            label: "Organização ID",
            type: "number",
            defaultValue: 1,
          },
          {
            name: "id_categoria_pai",
            label: "Categoria pai ID",
            type: "number",
          },
          { name: "codigo", label: "Código", required: true },
          { name: "nome", label: "Nome", required: true },
          { name: "descricao", label: "Descrição", type: "textarea" },
          {
            name: "metodo_depreciacao",
            label: "Método",
            defaultValue: "linha_reta",
          },
          {
            name: "vida_util_padrao_anos",
            label: "Vida útil padrão",
            type: "number",
            defaultValue: 5,
          },
          {
            name: "taxa_residual_padrao",
            label: "Taxa residual",
            type: "number",
            step: "0.01",
            defaultValue: 0,
          },
          {
            name: "ativo",
            label: "Ativa",
            defaultValue: "true",
            asBoolean: true,
          },
        ]}
        getItemKey={(item) => item.id}
        loadItems={erpApi.assets.listCategories}
        title="Categorias de ativos"
      />

      <EntityPanel
        columns={[
          { key: "id", label: "ID" },
          { key: "codigo", label: "Código" },
          { key: "nome", label: "Nome" },
          { key: "tipo_local", label: "Tipo" },
          { key: "endereco", label: "Endereço" },
          {
            key: "ativo",
            label: "Ativa",
            render: (item) => (item.ativo ? "Sim" : "Não"),
          },
        ]}
        createItem={erpApi.assets.createLocation}
        deleteItem={erpApi.assets.deleteLocation}
        fields={[
          {
            name: "id_organizacao",
            label: "Organização ID",
            type: "number",
            defaultValue: 1,
          },
          { name: "id_local_pai", label: "Local pai ID", type: "number" },
          { name: "codigo", label: "Código", required: true },
          { name: "nome", label: "Nome", required: true },
          { name: "tipo_local", label: "Tipo local" },
          { name: "endereco", label: "Endereço" },
          { name: "pessoa_contato", label: "Contato" },
          { name: "telefone_contato", label: "Telefone de contato" },
          {
            name: "ativo",
            label: "Ativa",
            defaultValue: "true",
            asBoolean: true,
          },
        ]}
        getItemKey={(item) => item.id}
        loadItems={erpApi.assets.listLocations}
        title="Localizações"
      />

      <EntityPanel
        columns={[
          { key: "id", label: "ID" },
          { key: "numero_tag", label: "Tag" },
          { key: "nome", label: "Nome" },
          { key: "id_categoria", label: "Categoria ID" },
          { key: "id_localizacao", label: "Localização ID" },
          { key: "status_ativo", label: "Status" },
          {
            key: "valor_atual",
            label: "Valor atual",
            render: (item) => formatCurrency(item.valor_atual),
          },
          {
            key: "data_criacao",
            label: "Criado em",
            render: (item) => formatDateTime(item.data_criacao),
          },
        ]}
        createItem={erpApi.assets.createAsset}
        deleteItem={erpApi.assets.deleteAsset}
        fields={[
          {
            name: "id_organizacao",
            label: "Organização ID",
            type: "number",
            defaultValue: 1,
          },
          {
            name: "id_categoria",
            label: "Categoria ID",
            type: "number",
            required: true,
          },
          {
            name: "id_localizacao",
            label: "Localização ID",
            type: "number",
            required: true,
          },
          { name: "id_fornecedor", label: "Fornecedor ID", type: "number" },
          { name: "numero_tag", label: "Número da tag", required: true },
          { name: "numero_serie", label: "Número de série" },
          { name: "nome", label: "Nome", required: true },
          { name: "modelo", label: "Modelo" },
          { name: "fabricante", label: "Fabricante" },
          { name: "descricao", label: "Descrição", type: "textarea" },
          { name: "status_ativo", label: "Status", defaultValue: "ativo" },
          { name: "criticidade", label: "Criticidade", defaultValue: "medio" },
          {
            name: "custo_aquisicao",
            label: "Custo de aquisição",
            type: "number",
            step: "0.01",
          },
          {
            name: "valor_residual",
            label: "Valor residual",
            type: "number",
            step: "0.01",
            defaultValue: 0,
          },
          {
            name: "valor_atual",
            label: "Valor atual",
            type: "number",
            step: "0.01",
          },
          { name: "observacoes", label: "Observações", type: "textarea" },
        ]}
        getItemKey={(item) => item.id}
        loadItems={erpApi.assets.listAssets}
        title="Ativos"
      />

      <section className="card">
        <h2>Gestao patrimonial</h2>
        <p>
          Este modulo concentra os principais registros necessários para
          acompanhar o patrimonio da organização, permitindo estruturar
          categorias, locais de alocação e ativos operacionais.
        </p>
      </section>
    </ModuleShell>
  );
}
