from sqlalchemy import (
    Column, Integer, String, Text, Date, Numeric,
    Sequence, CheckConstraint
)
from core.configs import DBBaseModel


class PlanoAcao(DBBaseModel):
    __tablename__ = "planos_acao"
    __table_args__ = (
        CheckConstraint(
            "status IN ('PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA')",
            name="planos_acao_status_check"
        ),
        CheckConstraint(
            "tipo_acao IN ('MITIGACAO', 'CONTINGENCIA', 'TRANSFERENCIA', 'ACEITACAO')",
            name="planos_acao_tipo_acao_check"
        ),
        {"schema": "grc"},
    )

    id = Column(Integer, Sequence("grc.planos_acao_id_seq"), primary_key=True)

    risco_id = Column(Integer, nullable=False)
    descricao = Column(Text, nullable=False)
    tipo_acao = Column(String(50))
    responsavel_id = Column(Integer, nullable=False)

    data_prevista_conclusao = Column(Date)
    data_conclusao = Column(Date)

    status = Column(String(20), default="PENDENTE", nullable=False)

    custo_estimado = Column(Numeric(15, 2))
    evidencia_conclusao = Column(Text)
