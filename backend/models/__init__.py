# __init__.py
from .sm_atendente_model import Atendente
from .sm_ticket_atendimento_model import TicketAtendimento
from .sm_solicitacao_troca_model import SolicitacaoTroca
from .sm_views_models import (
    VwDashboardServicos,
    VwTicketsAbertos,
    VwTrocasPendentes,
    VwHistoricoCliente,
    VwMetricasMensais,
    VwAnaliseTiposAtendimento,
    VwTempoResolucao,
    VwPerformanceAtendentes
)

__all__ = [
    "Atendente",
    "TicketAtendimento",
    "SolicitacaoTroca",
    "VwDashboardServicos",
    "VwTicketsAbertos",
    "VwTrocasPendentes",
    "VwHistoricoCliente",
    "VwMetricasMensais",
    "VwAnaliseTiposAtendimento",
    "VwTempoResolucao",
    "VwPerformanceAtendentes"
]