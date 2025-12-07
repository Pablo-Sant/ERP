from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class Beneficio(DBBaseModel):
    __tablename__ = "beneficios"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(200))
    valor = Column(Float)

    # Relacionamentos (já está correto)
    colaboradores = relationship("ColaboradorBeneficio", back_populates="beneficio")