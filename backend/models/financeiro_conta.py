from sqlalchemy import Column, Integer, String, Date, Text, Numeric, Boolean, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel
#from models.financeiro_extrato import FinanceirosExtratosBancarios

class FinanceiroContas(DBBaseModel):
    __tablename__ = "financeiro_contas"
    __table_args__ = {'schema': 'fi'}

    id_conta = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)
    saldo_inicial = Column(Numeric(14, 2), nullable=False, default=0)
    data_abertura = Column(Date, nullable=False)
    ativo = Column(Boolean, default=True)

    __table_args__ = (
        CheckConstraint("tipo IN ('caixa','banco','cartao')", name="financeiro_contas_tipo_check"),
        {'schema': 'fi'}
    )

    extratos = relationship("FinanceiroExtratosBancarios", back_populates="conta")
    lancamentos = relationship("FinanceiroLancamentos", back_populates="conta")
    orcamentos = relationship("FinanceiroOrcamentos", back_populates="conta")

