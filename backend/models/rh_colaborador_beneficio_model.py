from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class ColaboradorBeneficio(DBBaseModel):
    __tablename__ = "colaborador_beneficios"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, primary_key=True)
    colaborador_id = Column(Integer, ForeignKey("rh.colaboradores.id"), nullable=False)
    beneficio_id = Column(Integer, ForeignKey("rh.beneficios.id"), nullable=False)

    # Relacionamentos
    colaborador = relationship("Colaborador", back_populates="beneficios")
    beneficio = relationship("Beneficio", back_populates="colaboradores")