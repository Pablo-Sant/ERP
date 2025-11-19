from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, Sequence,
    CheckConstraint, ForeignKey, Numeric
)
from datetime import datetime
from core.configs import DBBaseModel

class OrdemProducao(DBBaseModel):
    __tablename__ = "ordens_producao"
    __table_args__ = (
        CheckConstraint(
            "prioridade IN ('BAIXA', 'NORMAL', 'ALTA', 'URGENTE')",
            name="ordens_producao_prioridade_check"
        ),
        CheckConstraint(
            "status IN ('PLANEJADA', 'LIBERADA', 'EM_PRODUCAO', 'PAUSADA', 'CONCLUIDA', 'CANCELADA')",
            name="ordens_producao_status_check"
        ),
        CheckConstraint("quantidade_planejada > 0", name="ordens_producao_quantidade_planejada_check"),
        {"schema": "pp"},
    )

    id = Column(Integer, Sequence("pp.ordens_producao_id_seq"), primary_key=True)
    numero_op = Column(String(50), nullable=False)
    produto_id = Column(Integer, nullable=False)
    quantidade_planejada = Column(Numeric(10, 2), nullable=False)
    quantidade_produzida = Column(Numeric(10, 2), default=0)
    quantidade_refugada = Column(Numeric(10, 2), default=0)
    prioridade = Column(String(20), default="NORMAL")
    data_emissao = Column(Date, default=datetime.now)
    data_inicio_prevista = Column(Date)
    data_fim_prevista = Column(Date)
    data_inicio_real = Column(Date)
    data_fim_real = Column(Date)
    status = Column(String(20), default="PLANEJADA")
    id_projeto = Column(Integer)
    observacoes = Column(Text)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now)