# ------------------- ATIVOS / AM -------------------
from models.ativos_model import Ativo
from models.am_pecas_ordem_servico import PecasOrdemServico
from models.am_planos_manutencao_model import PlanosManutencao
from models.am_registro_calibracao import RegistrosCalibracao
from models.registro_depreciacao import RegistrosDepreciacao

# ------------------- BI -------------------
from models.bi_cache_dados_model import CacheDadosBI
from models.bi_dashboard_model import Dashboard 
from models.bi_metrica_kpi_model import MetricaKPI

# ------------------- CONTABILIDADE -------------------
from models.contabilidade_lancamento import ContabilidadeLancamentos
from models.contabilidade_plano_conta import ContabilidadePlanoContas

# ------------------- CLIENTES / VC -------------------
from models.vc_contrato_model import Contrato
from models.vc_vendedor_model import Vendedor
from models.vc_cliente_final_model import ClienteFinal
from models.vc_historico_compra_model import HistoricoCompra
from models.vc_pedido_venda_model import PedidoVenda
from models.vc_prospecto_model import Prospecto


# ------------------- FISCAL -------------------
from models.fiscal_impostos import FiscalImpostos
from models.fiscal_notas_fiscais import FiscalNotasFiscais

# ------------------- FINANCEIRO -------------------
from models.financeiro_conta import FinanceiroContas
from models.financeiro_conciliacoes import FinanceiroConciliacoes
from models.financeiro_extrato import FinanceiroExtratosBancarios
from models.financeiro_fluxo_caixa import FinanceiroFluxoCaixa
from models.financeiro_lancamentos import FinanceiroLancamentos
from models.financeiro_orcamento import FinanceiroOrcamentos

# ------------------- GRC -------------------
from models.grc_audotorias_model import Auditoria
from models.grc_categorias_risco_model import CategoriaRisco
from models.grc_controles_internos_model import ControleInterno
from models.grc_nao_conformidade_model import NaoConformidadeAuditoria
from models.grc_planos_acao import PlanoAcao
from models.grc_requisitos_normativos import RequisitoNormativo
from models.grc_risco_controle import RiscoControle
from models.grc_riscos_corporativos_model import RiscoCorporativo
from models.grc_segregacao_funcoes import SegregacaoFuncoes
from models.grc_violacoes_sod import ViolacaoSoD

# ------------------- MM -------------------
from models.mm_armazens_model import Armazem
from models.mm_categorias_model import Categoria
from models.mm_empresas_model import Empresa
from models.mm_produto_model import Produto

# ------------------- ORDEM DE SERVIÇO / PRODUÇÃO -------------------
from models.ordens_servicos_model import OrdemServico
from models.pp_ordens_producao_model import OrdemProducao

# ------------------- PROJETOS -------------------
from models.projeto_model import ProjetoModel
from models.ps_riscos_projetos_model import RiscoProjeto

# ------------------- QM -------------------
from models.qm_ordem_inspecao_model import OrdemInspecao

# ------------------- SM (Suporte) -------------------
from models.sm_atendente_model import Atendente
from models.sm_ticket_atendimento_model import TicketAtendimento
from models.sm_solicitacao_troca_model import SolicitacaoTroca

# ------------------- USUÁRIOS -------------------
from models.usuario import UsuarioModel

# ------------------- RH -------------------
from models.rh_funcoes_model import Funcao
from models.rh_colaboradores_model import Colaborador
