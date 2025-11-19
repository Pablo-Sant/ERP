from sqlalchemy import (
    Column, Integer, String, Text, Date,
    Sequence, CheckConstraint
)
from core.configs import DBBaseModel


class RequisitoNormativo(DBBaseModel):
    __tablename__ = "requisitos_normativos"
    __table_args__ = (
        CheckConstraint(
            "status_conformidade IN ('CONFORME', 'NAO_CONFORME', 'NAO_AVALIADO', 'EM_AVALIACAO')",
            name="requisitos_normativos_status_conformidade_check"
        ),
        {"schema": "grc"},
    )

    id = Column(Integer, Sequence("grc.requisitos_normativos_id_seq"), primary_key=True)

    norma = Column(String(200), nullable=False)
    versao = Column(String(50))
    item_norma = Column(String(100))
    descricao_requisito = Column(Text, nullable=False)

    data_publicacao = Column(Date)
    data_validade = Column(Date)

    responsavel_conformidade_id = Column(Integer)

    status_conformidade = Column(
        String(20),
        default="NAO_AVALIADO",
        nullable=False,
    )
