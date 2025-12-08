from sqlalchemy import Column, Integer, String, Date, Text, Numeric, Boolean, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel



class FinanceiroExtratosBancarios(DBBaseModel):
    __tablename__ = "financeiro_extratos_bancarios"
    __table_args__ = {'schema': 'fi'}

    id_extrato = Column(Integer, primary_key=True, autoincrement=True)
    id_conta = Column(Integer, ForeignKey("fi.financeiro_contas.id_conta"), nullable=False)
    data_movimento = Column(Date, nullable=False)
    descricao = Column(Text)
    valor = Column(Numeric(14, 2), nullable=False)
    tipo = Column(String(10), nullable=False)
    conciliado = Column(Boolean, default=False)

    __table_args__ = (
        CheckConstraint("tipo IN ('credito','debito')", name="financeiro_extratos_bancarios_tipo_check"),
        {'schema': 'fi'}
    )

    #conta = relationship("FinanceiroContas", back_populates="extratos")
   # conciliacoes = relationship("FinanceiroConciliacoes", back_populates="extrato")