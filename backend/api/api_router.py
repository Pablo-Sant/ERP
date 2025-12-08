from fastapi import APIRouter

api_router = APIRouter()

# ==================== ATIVOS ====================
from api.v1.endpoints import (
    categoria_ativo, documento_ativo, localizacao, 
    metrica_ativo, movimentacao_ativo, ativos
)

api_router.include_router(
    ativos.router,
    prefix="/ativos",
    tags=["Ativos - ativos"]
)

api_router.include_router(
    categoria_ativo.router,
    prefix="/ativos/categorias",
    tags=["Ativos - Categorias"]
)

api_router.include_router(
    documento_ativo.router,
    prefix="/ativos/documentos",
    tags=["Ativos - Documentos"]
)

api_router.include_router(
    localizacao.router,
    prefix="/ativos/localizacoes",
    tags=["Ativos - Localizações"]
)

api_router.include_router(
    metrica_ativo.router,
    prefix="/ativos/metricas",
    tags=["Ativos - Métricas"]
)

api_router.include_router(
    movimentacao_ativo.router,
    prefix="/ativos/movimentacoes",
    tags=["Ativos - Movimentações"]
)

# ==================== BI ====================
from api.v1.endpoints import (
    bi_cache_dados, bi_dashboard, bi_metrica_KPI
)

api_router.include_router(
    bi_cache_dados.router,
    prefix="/bi/cache",
    tags=["BI - Cache"]
)

api_router.include_router(
    bi_dashboard.router,
    prefix="/bi/dashboards",
    tags=["BI - Dashboards"]
)

api_router.include_router(
    bi_metrica_KPI.router,
    prefix="/bi/kpis",
    tags=["BI - KPIs"]
)

# ==================== CONTABILIDADE ====================
from api.v1.endpoints import (
    contabilidade_lancamento, contabilidade_plano_conta
)

api_router.include_router(
    contabilidade_lancamento.router,
    prefix="/contabilidade/lancamentos",
    tags=["Contabilidade - Lançamentos"]
)

api_router.include_router(
    contabilidade_plano_conta.router,
    prefix="/contabilidade/planos-contas",
    tags=["Contabilidade - Planos de Contas"]
)

# ==================== FINANCEIRO ====================
from api.v1.endpoints import (
    financeiro_conta, financeiro_extrato, financeiro_fluxo_caixa,
    financeiro_conciliacoes, financeiro_orcamento
)

api_router.include_router(
    financeiro_conta.router,
    prefix="/financeiro/contas",
    tags=["Financeiro - Contas"]
)

api_router.include_router(
    financeiro_extrato.router,
    prefix="/financeiro/extratos",
    tags=["Financeiro - Extratos"]
)

api_router.include_router(
    financeiro_fluxo_caixa.router,
    prefix="/financeiro/fluxo-caixa",
    tags=["Financeiro - Fluxo de Caixa"]
)

api_router.include_router(
    financeiro_conciliacoes.router,
    prefix="/financeiro/conciliacoes",
    tags=["Financeiro - Conciliações"]
)

api_router.include_router(
    financeiro_orcamento.router,
    prefix="/financeiro/orcamentos",
    tags=["Financeiro - Orçamentos"]
)

# ==================== FISCAL ====================
from api.v1.endpoints import (
    fiscal_impostos, fiscal_notas_fiscais
)

api_router.include_router(
    fiscal_impostos.router,
    prefix="/fiscal/impostos",
    tags=["Fiscal - Impostos"]
)

api_router.include_router(
    fiscal_notas_fiscais.router,
    prefix="/fiscal/notas-fiscais",
    tags=["Fiscal - Notas Fiscais"]
)

# ==================== GRC ====================
from api.v1.endpoints import (
    grc_auditorias, grc_categorias_risco, grc_controles_internos,
    grc_nao_conformidade, grc_planos_acao
)

api_router.include_router(
    grc_auditorias.router,
    prefix="/grc/auditorias",
    tags=["GRC - Auditorias"]
)

api_router.include_router(
    grc_categorias_risco.router,
    prefix="/grc/categorias-risco",
    tags=["GRC - Categorias de Risco"]
)

api_router.include_router(
    grc_controles_internos.router,
    prefix="/grc/controles-internos",
    tags=["GRC - Controles Internos"]
)

api_router.include_router(
    grc_nao_conformidade.router,
    prefix="/grc/nao-conformidades",
    tags=["GRC - Não Conformidades"]
)

api_router.include_router(
    grc_planos_acao.router,
    prefix="/grc/planos-acao",
    tags=["GRC - Planos de Ação"]
)

# ==================== MATERIAIS (MM) ====================
from api.v1.endpoints import (
    mm_armazens, mm_categorias, mm_empresas, mm_produto
)

api_router.include_router(
    mm_armazens.router,
    prefix="/materiais/armazens",
    tags=["Materiais - Armazéns"]
)

api_router.include_router(
    mm_categorias.router,
    prefix="/materiais/categorias",
    tags=["Materiais - Categorias"]
)

api_router.include_router(
    mm_empresas.router,
    prefix="/materiais/empresas",
    tags=["Materiais - Empresas"]
)

api_router.include_router(
    mm_produto.router,
    prefix="/materiais/produtos",
    tags=["Materiais - Produtos"]
)

# ==================== ORDENS DE SERVIÇO ====================
from api.v1.endpoints import ordens_servico

api_router.include_router(
    ordens_servico.router,
    prefix="/ordens-servico",
    tags=["Ordens de Serviço"]
)

# ==================== PRODUTOS ====================
from api.v1.endpoints import produto

api_router.include_router(
    produto.router,
    prefix="/produtos",
    tags=["Produtos"]
)

# ==================== RH ====================
from api.v1.endpoints import (
    rh_avaliacao_desempenho, rh_beneficios, rh_folha_pagamento,
    rh_funcoes, rh_recrutamento, colaborador, colaborador_beneficio
)

api_router.include_router(
    rh_avaliacao_desempenho.router,
    prefix="/rh/avaliacoes-desempenho",
    tags=["RH - Avaliações de Desempenho"]
)

api_router.include_router(
    rh_beneficios.router,
    prefix="/rh/beneficios",
    tags=["RH - Benefícios"]
)

api_router.include_router(
    rh_folha_pagamento.router,
    prefix="/rh/folha-pagamento",
    tags=["RH - Folha de Pagamento"]
)

api_router.include_router(
    rh_funcoes.router,
    prefix="/rh/funcoes",
    tags=["RH - Funções"]
)

api_router.include_router(
    rh_recrutamento.router,
    prefix="/rh/recrutamento",
    tags=["RH - Recrutamento"]
)

api_router.include_router(
    colaborador.router,
    prefix="/rh/colaboradores",
    tags=["RH - Colaboradores"]
)

api_router.include_router(
    colaborador_beneficio.router,
    prefix="/rh/colaboradores-beneficios",
    tags=["RH - Benefícios de Colaboradores"]
)

# ==================== VENDAS E COMPRAS (VC) ====================
from api.v1.endpoints import (
    vc_cliente_final, vc_contrato, 
    vc_historico_compra, vc_pedido_venda
)

# NOTA: Removi o roteador "cliente_final" que estava duplicado
# e mantive apenas "vc_cliente_final" para consistência

api_router.include_router(
    vc_cliente_final.router,
    prefix="/vendas-compras/clientes",
    tags=["Vendas e Compras - Clientes"]
)

api_router.include_router(
    vc_contrato.router,
    prefix="/vendas-compras/contratos",
    tags=["Vendas e Compras - Contratos"]
)

api_router.include_router(
    vc_historico_compra.router,
    prefix="/vendas-compras/historico-compras",
    tags=["Vendas e Compras - Histórico de Compras"]
)

api_router.include_router(
    vc_pedido_venda.router,
    prefix="/vendas-compras/pedidos-venda",
    tags=["Vendas e Compras - Pedidos de Venda"]
)

# ==================== FORNECEDORES ====================
from api.v1.endpoints import fornecedor

api_router.include_router(
    fornecedor.router,
    prefix="/fornecedores",
    tags=["Fornecedores"]
)

# NOTA: Removi as importações duplicadas e os roteadores redundantes