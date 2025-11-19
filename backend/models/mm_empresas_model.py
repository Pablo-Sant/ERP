from sqlalchemy import (
    Column, Integer, String, DateTime, Sequence
)
from datetime import datetime
from core.configs import DBBaseModel


class Empresa(DBBaseModel):
    __tablename__ = "empresas"
    __table_args__ = (
        {"schema": "mm"},
    )

    id = Column(Integer, Sequence("mm.empresas_id_seq"), primary_key=True)

    nome = Column(String(255), nullable=False)
    cpf_cnpj = Column(String(20))

    data_criacao = Column(DateTime, default=datetime.now)
