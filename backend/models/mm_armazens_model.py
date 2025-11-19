from sqlalchemy import (
    Column, Integer, String, Text, Sequence
)
from core.configs import DBBaseModel


class Armazem(DBBaseModel):
    __tablename__ = "armazens"
    __table_args__ = (
        {"schema": "mm"},
    )

    id = Column(Integer, Sequence("mm.armazens_id_seq"), primary_key=True)

    empresa_id = Column(Integer, nullable=False)
    nome = Column(String(255), nullable=False)
    endereco = Column(Text)
