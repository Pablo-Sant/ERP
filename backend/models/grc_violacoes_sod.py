from sqlalchemy import (
    Column, Integer, String, Date, Sequence,
    CheckConstraint
)
from core.configs import DBBaseModel


class ViolacaoSoD(DBBaseModel):
    __tablename__ = "violacoes_sod"
    __table_args__ = (
        CheckConstraint(
            "status IN ('PENDENTE', 'RESOLVIDA', 'EXCEPCIONAL_APROVADA')",
            name="violacoes_sod_status_check"
        ),
        {"schema": "grc"},
    )

    id = Column(Integer, Sequence("grc.violacoes_sod_id_seq"), primary_key=True)

    usuario_id = Column(Integer, nullable=False)

    funcao_conflitante_1 = Column(String(100))
    funcao_conflitante_2 = Column(String(100))

    data_deteccao = Column(Date)
    status = Column(String(20), default="PENDENTE")
