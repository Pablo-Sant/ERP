from sqlalchemy import Column, Integer, String, Date, Text, Numeric, Boolean, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel
from models.financeiro_conta import FinanceiroContas

class FinanceiroOrcamentos(DBBaseModel):
    __tablename__ = "financeiro_orcamentos"

    id_orcamento = Column(Integer, primary_key=True, autoincrement=True)
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    id_conta = Column(Integer, ForeignKey("fi.financeiro_contas.id_conta"), nullable=False)
    valor_previsto = Column(Numeric(14, 2), nullable=False)
    valor_realizado = Column(Numeric(14, 2), default=0)

   """ __table_args__ = (
        CheckConstraint("mes >= 1 AND mes <= 12", name="financeiro_orcamentos_mes_check"),
        {'schema': 'fi'}
    )"""

    #conta = relationship("FinanceiroContas", back_populates="orcamentos")