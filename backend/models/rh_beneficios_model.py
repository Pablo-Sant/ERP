from sqlalchemy import Column, Integer, String, Float, Sequence
from core.configs import DBBaseModel

class Beneficio(DBBaseModel):
    __tablename__ = "beneficios"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, Sequence("rh.beneficios_id_seq"), primary_key=True)

    nome = Column(String(50), nullable=False)
    descricao = Column(String(200))
    valor = Column(Float)
    