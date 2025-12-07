from fastapi import APIRouter
from api.v1.endpoints import cliente_final
from api.v1.endpoints import colaborador
from api.v1.endpoints import colaborador_beneficio
from api.v1.endpoints import contrato
from api.v1.endpoints import contabilidade_lancamento
from api.v1.endpoints import contabilidade_plano_conta
from api.v1.endpoints import financeiro_conta
from api.v1.endpoints import financeiro_extrato
from api.v1.endpoints import financeiro_fluxo_caixa
from api.v1.endpoints import financeiro_conciliacoes
from api.v1.endpoints import financeiro_orcamento
from api.v1.endpoints import fiscal_impostos
from api.v1.endpoints import fiscal_notas_fiscais
from api.v1.endpoints import fornecedor
from api.v1.endpoints import grc_auditorias
from api.v1.endpoints import grc_categorias_risco
from api.v1.endpoints import grc_controles_internos
from api.v1.endpoints import grc_nao_conformidade
from api.v1.endpoints import grc_planos_acao
from api.v1.endpoints import bi_cache_dados
from api.v1.endpoints import bi_dashboard
from api.v1.endpoints import bi_metrica_KPI
from api.v1.endpoints import categoria_ativo
from api.v1.endpoints import documento_ativo
from api.v1.endpoints import localizacao
from api.v1.endpoints import metrica_ativo
from api.v1.endpoints import mm_armazens, mm_categorias, mm_empresas, mm_produto
from api.v1.endpoints import movimentacao_ativo
from api.v1.endpoints import ordens_servico
from api.v1.endpoints import produto
from api.v1.endpoints import rh_avaliacao_desempenho
from api.v1.endpoints import rh_beneficios
from api.v1.endpoints import rh_folha_pagamento
from api.v1.endpoints import rh_funcoes
from api.v1.endpoints import rh_recrutamento
from api.v1.endpoints import vc_cliente_final
from api.v1.endpoints import vc_contrato
from api.v1.endpoints import vc_historico_compra
from api.v1.endpoints import vc_pedido_venda

api_router = APIRouter()

# Cliente final

api_router.include_router(
    cliente_final.router, 
    prefix="/clientes", 
    tags=["Clientes"]
)

# RH

api_router.include_router(
    colaborador.router, 
    prefix="/colaboradores", 
    tags=["Colaboradores"]
)

api_router.include_router(
    colaborador_beneficio.router, 
    prefix="/colaborador-beneficio", 
    tags=["Benefícios de Colaboradores"]
)

# Contratos

api_router.include_router(
    contrato.router, 
    prefix="/contratos", 
    tags=["Contratos"]
)

# Contabilidade

api_router.include_router(
    contabilidade_lancamento.router, 
    prefix="/contabilidade/lancamentos", 
    tags=["Contabilidade - Lançamentos"]
)

api_router.include_router(
    contabilidade_plano_conta.router, 
    prefix="/contabilidade/planocontas", 
    tags=["Contabilidade - Plano de Contas"]
)


# Financeiro

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
    prefix="/financeiro/fluxocaixa", 
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

# Fiscal

api_router.include_router(
    fiscal_impostos.router, 
    prefix="/fiscal/impostos", 
    tags=["Fiscal - Impostos"]
)

api_router.include_router(
    fiscal_notas_fiscais.router, 
    prefix="/fiscal/notas", 
    tags=["Fiscal - Notas Fiscais"]
)

# Fornecedores

api_router.include_router(
    fornecedor.router, 
    prefix="/fornecedores", 
    tags=["Fornecedores"]
)

# GRC 

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

# BI

api_router.include_router(
    bi_cache_dados.router, 
    prefix="/bi/cache-dados", 
    tags=["Business Intelligence - Cache"]
)

api_router.include_router(
    bi_dashboard.router, 
    prefix="/bi/dashboards", 
    tags=["Business Intelligence - Dashboard"]
)

api_router.include_router(
    bi_metrica_KPI.router, 
    prefix="/bi/kpi", 
    tags=["Business Intelligence - KPI"]
)

# ATIVOS

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


# localização
api_router.include_router(
    localizacao.router,
    prefix="/localizacao",
    tags=["localização"]
)

# métricas de ativos
api_router.include_router(
    metrica_ativo.router,
    prefix="/ativos/metricas",
    tags=["métricas de ativos"]
)

# materiais
api_router.include_router(
    mm_armazens.router,
    prefix="/mm/armazens",
    tags=["materiais - armazens"]
)

api_router.include_router(
    mm_categorias.router,
    prefix="/mm/categorias",
    tags=["materiais - categorias"]
)

api_router.include_router(
    mm_empresas.router,
    prefix="/mm/empresas",
    tags=["materiais - empresas"]
)

api_router.include_router(
    mm_produto.router,
    prefix="/mm/produtos",
    tags=["materiais - produtos"]
)

# movimentação de ativos
api_router.include_router(
    movimentacao_ativo.router,
    prefix="/ativos/movimentacoes",
    tags=["movimentação de ativos"]
)

# ordens de serviço
api_router.include_router(
    ordens_servico.router,
    prefix="/ordens-servico",
    tags=["ordens de serviço"]
)

# produto (genérico)
api_router.include_router(
    produto.router,
    prefix="/produtos",
    tags=["produtos"]
)

# rh
api_router.include_router(
    rh_avaliacao_desempenho.router,
    prefix="/rh/avaliacoes-desempenho",
    tags=["rh - avaliação de desempenho"]
)

api_router.include_router(
    rh_beneficios.router,
    prefix="/rh/beneficios",
    tags=["rh - benefícios"]
)

api_router.include_router(
    rh_folha_pagamento.router,
    prefix="/rh/folha-pagamento",
    tags=["rh - folha de pagamento"]
)

api_router.include_router(
    rh_funcoes.router,
    prefix="/rh/funcoes",
    tags=["rh - funções"]
)

api_router.include_router(
    rh_recrutamento.router,
    prefix="/rh/recrutamento",
    tags=["rh - recrutamento"]
)

# vendas e compras 
api_router.include_router(
    vc_cliente_final.router,
    prefix="/vc/clientes",
    tags=["vendas e compras - clientes"]
)

api_router.include_router(
    vc_contrato.router,
    prefix="/vc/contratos",
    tags=["vendas e compras - contratos"]
)

api_router.include_router(
    vc_historico_compra.router,
    prefix="/vc/historico-compras",
    tags=["vendas e compras - histórico de compras"]
)

api_router.include_router(
    vc_pedido_venda.router,
    prefix="/vc/pedidos-venda",
    tags=["vendas e compras - pedidos de venda"]
)


