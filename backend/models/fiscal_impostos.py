from sqlalchemy import Column, Integer, String, Date, Text, Numeric, Boolean, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel
from models.fiscal_notas_fiscais import FiscalNotasFiscais

class FiscalImpostos(DBBaseModel):
    __tablename__ = "fiscal_impostos"
    __table_args__ = {'schema': 'fi'}

    id_imposto = Column(Integer, primary_key=True, autoincrement=True)
    id_nota = Column(Integer, ForeignKey("fi.fiscal_notas_fiscais.id_nota"), nullable=False)
    tipo_imposto = Column(String(20), nullable=False)
    base_calculo = Column(Numeric(14, 2), nullable=False)
    aliquota = Column(Numeric(5, 2), nullable=False)
    valor = Column(Numeric(14, 2), nullable=False)

    nota = relationship("FiscalNotasFiscais", back_populates="impostos")