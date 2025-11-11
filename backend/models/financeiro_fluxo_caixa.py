from sqlalchemy import Column, Integer, String, Date, Text, Numeric, Boolean, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class FinanceiroFluxoCaixa(DBBaseModel):
    __tablename__ = "financeiro_fluxo_caixa"
    __table_args__ = {'schema': 'fi'}

    id_fluxo = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    saldo_inicial = Column(Numeric(14, 2), nullable=False)
    entradas = Column(Numeric(14, 2), nullable=False)
    saidas = Column(Numeric(14, 2), nullable=False)
    saldo_final = Column(Numeric(14, 2), nullable=False)