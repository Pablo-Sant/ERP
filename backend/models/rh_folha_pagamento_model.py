from sqlalchemy import Column, Integer, Float, Sequence
from core.configs import DBBaseModel

class FolhaPagamento(DBBaseModel):
    __tablename__ = "folha_pagamento"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, Sequence("rh.folha_pagamento_id_seq"), primary_key=True)

    colaborador_id = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)

    salario_base = Column(Float, nullable=False)
    descontos = Column(Float)
    salario_liquido = Column(Float, nullable=False)
        