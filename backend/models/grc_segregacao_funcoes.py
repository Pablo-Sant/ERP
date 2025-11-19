from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    Date, Sequence, CheckConstraint
)
from core.configs import DBBaseModel


class SegregacaoFuncoes(DBBaseModel):
    __tablename__ = "segregacao_funcoes"
    __table_args__ = (
        CheckConstraint(
            "conflito_nivel IN ('CRITICO', 'ALTO', 'MEDIO', 'BAIXO')",
            name="segregacao_funcoes_conflito_nivel_check"
        ),
        {"schema": "grc"},
    )

    id = Column(Integer, Sequence("grc.segregacao_funcoes_id_seq"), primary_key=True)

    funcao_1 = Column(String(100), nullable=False)
    funcao_2 = Column(String(100), nullable=False)

    conflito_nivel = Column(String(20))
    justificativa = Column(Text)

    aprovado = Column(Boolean, default=False)
    data_aprovacao = Column(Date)
