from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class Funcao(DBBaseModel):
    __tablename__ = "funcoes"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(200))

    
    colaboradores = relationship("Colaborador", back_populates="funcao_rel")