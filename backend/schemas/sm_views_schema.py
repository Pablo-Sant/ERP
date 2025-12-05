# sm_views_schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# Schemas para VwDashboardServicos
class DashboardServicosResponse(BaseModel):
    tickets_abertos: int
    tickets_hoje: int
    trocas_pendentes: int
    total_atendentes: int
    tempo_medio_resolucao_30_dias: Optional[float] = None

# Schemas para VwTicketsAbertos
class TicketAbertoResponse(BaseModel):
    id_ticket: int
    cliente: str
    assunto: str
    tipo: Optional[str] = None
    prioridade: str
    data_abertura: datetime
    tempo_aberto: str
    
    class Config:
        orm_mode = True
        from_attributes = True

# Schemas para VwTrocasPendentes
class TrocaPendenteResponse(BaseModel):
    id_solicitacao: int
    cliente: str
    assunto: str
    motivo: Optional[str] = None
    status_troca: str
    data_solicitacao: datetime
    id_pedido: Optional[int] = None
    vendedor_original: Optional[str] = None
    
    class Config:
        orm_mode = True
        from_attributes = True

# Schemas para VwHistoricoCliente
class HistoricoClienteResponse(BaseModel):
    cliente_finalid: int
    cliente: str
    data_ultima_compra: Optional[date] = None
    total_tickets: int
    tickets_resolvidos: int
    solicitacoes_troca: int
    solicitacoes_garantia: int
    ultimo_ticket: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        from_attributes = True

# Schemas para VwMetricasMensais
class MetricasMensaisResponse(BaseModel):
    mes: datetime
    ano: int
    mes_numero: int
    total_tickets: int
    tickets_resolvidos: int
    trocas_solicitadas: int
    garantias_solicitadas: int
    taxa_resolucao_percentual: Optional[float] = None
    
    class Config:
        orm_mode = True
        from_attributes = True

# Schemas para VwAnaliseTiposAtendimento
class AnaliseTiposAtendimentoResponse(BaseModel):
    tipo: str
    total_tickets: int
    tempo_medio_horas: Optional[float] = None
    percentual: Optional[float] = None
    
    class Config:
        orm_mode = True
        from_attributes = True

# Schemas para VwTempoResolucao
class TempoResolucaoResponse(BaseModel):
    prioridade: str
    total_tickets: int
    tempo_minimo_horas: Optional[float] = None
    tempo_maximo_horas: Optional[float] = None
    tempo_medio_horas: Optional[float] = None
    
    class Config:
        orm_mode = True
        from_attributes = True

# Schemas para VwPerformanceAtendentes
class PerformanceAtendentesResponse(BaseModel):
    id_atendente: int
    atendente: str
    setor: Optional[str] = None
    observacao: str
    
    class Config:
        orm_mode = True
        from_attributes = True