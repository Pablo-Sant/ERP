from sqlalchemy import (
    Column, Integer, String, Text, Date,
    Sequence, CheckConstraint, Computed
)
from core.configs import DBBaseModel


class RiscoProjeto(DBBaseModel):
    __tablename__ = "riscos_projeto"
    __table_args__ = (
        CheckConstraint(
            "status IN ('ABERTO', 'MONITORANDO', 'MITIGADO', 'RESOLVIDO', 'CANCELADO')",
            name="riscos_projeto_status_check"
        ),
        CheckConstraint(
            "impacto >= 1 AND impacto <= 5",
            name="riscos_projeto_impacto_check"
        ),
        CheckConstraint(
            "probabilidade >= 1 AND probabilidade <= 5",
            name="riscos_projeto_probabilidade_check"
        ),
        {"schema": "ps"},
    )

    id_risco = Column(Integer, Sequence("ps.riscos_projeto_id_risco_seq"), primary_key=True)

    id_projeto = Column(Integer, nullable=False)

    descricao = Column(Text, nullable=False)

    probabilidade = Column(Integer)
    impacto = Column(Integer)

    
    severidade = Column(
        Integer,
        Computed("probabilidade * impacto", persisted=True)
    )

    plano_mitigacao = Column(Text)

    id_responsavel = Column(Integer)

    status = Column(String(50), default="ABERTO")

    data_deteccao = Column(Date)
    data_resolucao = Column(Date)
