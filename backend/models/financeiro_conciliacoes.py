from sqlalchemy import Column, Integer, String, Date, Text, Numeric, Boolean, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class FinanceiroConciliacoes(DBBaseModel):
    __tablename__ = "financeiro_conciliacoes"
    __table_args__ = {'schema': 'fi'}

    id_conciliacao = Column(Integer, primary_key=True, autoincrement=True)
    id_extrato = Column(Integer, ForeignKey("fi.financeiro_extratos_bancarios.id_extrato"), nullable=False)
    id_lancamento = Column(Integer, ForeignKey("fi.financeiro_lancamentos.id_lancamento"))
    data_conciliacao = Column(TIMESTAMP, default=None)

    extrato = relationship("FinanceiroExtratosBancarios", back_populates="conciliacoes")
    lancamento = relationship("FinanceiroLancamentos", back_populates="conciliacoes")