from sqlalchemy import (
    Column, Integer, String, Text,
    Sequence, CheckConstraint
)
from core.configs import DBBaseModel


class RiscoControle(DBBaseModel):
    __tablename__ = "risco_controle"
    __table_args__ = (
        CheckConstraint(
            "eficacia_mitigacao IN ('ALTA', 'MEDIA', 'BAIXA')",
            name="risco_controle_eficacia_mitigacao_check"
        ),
        {"schema": "grc"},
    )

    id = Column(Integer, Sequence("grc.risco_controle_id_seq"), primary_key=True)

    risco_id = Column(Integer, nullable=False)
    controle_id = Column(Integer, nullable=False)

    eficacia_mitigacao = Column(String(20))
    observacoes = Column(Text)
