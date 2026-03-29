import React, { useEffect, useState } from "react";
import ModuleShell from "../components/ModuleShell";
import { erpApi } from "../services/erpApi";
import { getErrorMessage } from "../services/api";

const cards = [
  {
    key: "materials",
    label: "Produtos",
    loader: () => erpApi.materials.listProducts(),
  },
  {
    key: "financial",
    label: "Contas Financeiras",
    loader: () => erpApi.financial.listAccounts(),
  },
  { key: "assets", label: "Ativos", loader: () => erpApi.assets.listAssets() },
  {
    key: "hr",
    label: "Colaboradores",
    loader: () => erpApi.hr.listEmployees(),
  },
  { key: "sales", label: "Clientes", loader: () => erpApi.sales.listClients() },
  { key: "bi", label: "Dashboards", loader: () => erpApi.bi.listDashboards() },
];

export default function Dashboard() {
  const [stats, setStats] = useState({});
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadStats() {
      const results = await Promise.allSettled(
        cards.map((card) => card.loader()),
      );
      const nextStats = {};
      let firstError = "";

      results.forEach((result, index) => {
        const card = cards[index];
        if (result.status === "fulfilled") {
          nextStats[card.key] = result.value.data.length;
        } else {
          nextStats[card.key] = "-";
          if (!firstError) {
            firstError = getErrorMessage(
              result.reason,
              "Falha ao carregar indicadores do painel.",
            );
          }
        }
      });

      setStats(nextStats);
      setError(firstError);
    }

    loadStats();
  }, []);

  return (
    <ModuleShell
      description="Visão consolidada dos principais registros disponiveis nos modulos do BluERP."
      title="Dashboard"
    >
      {error ? <div className="alert alert-danger">{error}</div> : null}
      <section className="dashboard-grid">
        {cards.map((card) => (
          <article className="card dashboard-card" key={card.key}>
            <h2>{card.label}</h2>
            <p className="dashboard-metric">{stats[card.key] ?? "..."}</p>
          </article>
        ))}
      </section>
      <section className="card">
        <h2>Panorama operacional</h2>
        <p>
          Este painel apresenta um resumo inicial da base de dados por area,
          facilitando a navegação entre os módulos e oferecendo uma leitura
          rapida do volume de registros do sistema.
        </p>
      </section>
    </ModuleShell>
  );
}
