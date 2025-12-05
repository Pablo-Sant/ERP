# sm_views_models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from core.configs import DBBaseModel
from datetime import datetime, date

# View: vw_dashboard_servicos
class VwDashboardServicos(DBBaseModel):
    __tablename__ = "vw_dashboard_servicos"
    __table_args__ = {"schema": "sm"}
    
    tickets_abertos = Column(Integer)
    tickets_hoje = Column(Integer)
    trocas_pendentes = Column(Integer)
    total_atendentes = Column(Integer)
    tempo_medio_resolucao_30_dias = Column(Float)

# View: vw_tickets_abertos
class VwTicketsAbertos(DBBaseModel):
    __tablename__ = "vw_tickets_abertos"
    __table_args__ = {"schema": "sm"}
    
    id_ticket = Column(Integer, primary_key=True)
    cliente = Column(String(100))
    assunto = Column(String(100))
    tipo = Column(String(50))
    prioridade = Column(String(20))
    data_abertura = Column(DateTime)
    tempo_aberto = Column(String)  # O tipo interval do PostgreSQL é retornado como string

# View: vw_trocas_pendentes
class VwTrocasPendentes(DBBaseModel):
    __tablename__ = "vw_trocas_pendentes"
    __table_args__ = {"schema": "sm"}
    
    id_solicitacao = Column(Integer, primary_key=True)
    cliente = Column(String(100))
    assunto = Column(String(100))
    motivo = Column(String(100))
    status_troca = Column(String(20))
    data_solicitacao = Column(DateTime)
    id_pedido = Column(Integer)
    vendedor_original = Column(String(100))

# View: vw_historico_cliente
class VwHistoricoCliente(DBBaseModel):
    __tablename__ = "vw_historico_cliente"
    __table_args__ = {"schema": "sm"}
    
    cliente_finalid = Column(Integer, primary_key=True)
    cliente = Column(String(100))
    data_ultima_compra = Column(Date)
    total_tickets = Column(Integer)
    tickets_resolvidos = Column(Integer)
    solicitacoes_troca = Column(Integer)
    solicitacoes_garantia = Column(Integer)
    ultimo_ticket = Column(DateTime)

# View: vw_metricas_mensais
class VwMetricasMensais(DBBaseModel):
    __tablename__ = "vw_metricas_mensais"
    __table_args__ = {"schema": "sm"}
    
    mes = Column(DateTime, primary_key=True)
    ano = Column(Integer)
    mes_numero = Column(Integer)
    total_tickets = Column(Integer)
    tickets_resolvidos = Column(Integer)
    trocas_solicitadas = Column(Integer)
    garantias_solicitadas = Column(Integer)
    taxa_resolucao_percentual = Column(Float)

# View: vw_analise_tipos_atendimento
class VwAnaliseTiposAtendimento(DBBaseModel):
    __tablename__ = "vw_analise_tipos_atendimento"
    __table_args__ = {"schema": "sm"}
    
    tipo = Column(String(50), primary_key=True)
    total_tickets = Column(Integer)
    tempo_medio_horas = Column(Float)
    percentual = Column(Float)

# View: vw_tempo_resolucao
class VwTempoResolucao(DBBaseModel):
    __tablename__ = "vw_tempo_resolucao"
    __table_args__ = {"schema": "sm"}
    
    prioridade = Column(String(20), primary_key=True)
    total_tickets = Column(Integer)
    tempo_minimo_horas = Column(Float)
    tempo_maximo_horas = Column(Float)
    tempo_medio_horas = Column(Float)

# View: vw_performance_atendentes
class VwPerformanceAtendentes(DBBaseModel):
    __tablename__ = "vw_performance_atendentes"
    __table_args__ = {"schema": "sm"}
    
    id_atendente = Column(Integer, primary_key=True)
    atendente = Column(String(100))
    setor = Column(String(50))
    observacao = Column(String(50))