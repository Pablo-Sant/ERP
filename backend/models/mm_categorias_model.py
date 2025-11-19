from sqlalchemy import (
    Column, Integer, String, Text, Sequence
)
from core.configs import DBBaseModel


class Categoria(DBBaseModel):
    __tablename__ = "categorias"
    __table_args__ = (
        {"schema": "mm"},
    )

    id = Column(Integer, Sequence("mm.categorias_id_seq"), primary_key=True)

    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    categoria_pai_id = Column(Integer)
