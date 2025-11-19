from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Sequence
)
from datetime import datetime
from core.configs import DBBaseModel


class Produto(DBBaseModel):
    __tablename__ = "produtos"
    __table_args__ = (
        {"schema": "mm"},
    )

    id = Column(Integer, Sequence("mm.produtos_id_seq"), primary_key=True)

    empresa_id = Column(Integer, nullable=False)
    categoria_id = Column(Integer, nullable=False)

    nome = Column(String(255), nullable=False)
    descricao = Column(Text)

    data_criacao = Column(DateTime, default=datetime.now)
    data_atualizacao = Column(DateTime, default=datetime.now)
