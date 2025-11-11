from sqlalchemy import Column, Integer, String, Date, Text, Numeric, Boolean, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel
from models.financeiro_conta import FinanceiroContas
from models.financeiro_conciliacoes import FinanceiroConciliacoes

class FinanceiroLancamentos(DBBaseModel):
    __tablename__ = "financeiro_lancamentos"
    __table_args__ = {'schema': 'fi'}

    id_lancamento = Column(Integer, primary_key=True, autoincrement=True)
    id_conta = Column(Integer, ForeignKey("fi.financeiro_contas.id_conta"), nullable=False)
    tipo = Column(String(10), nullable=False)
    valor = Column(Numeric(14, 2), nullable=False)
    descricao = Column(Text)
    data_lancamento = Column(Date, nullable=False)
    origem_modulo = Column(String(50))
    origem_id = Column(Integer)
    created_at = Column(TIMESTAMP)

    __table_args__ = (
        CheckConstraint("tipo IN ('receita','despesa')", name="financeiro_lancamentos_tipo_check"),
        {'schema': 'fi'}
    )

    conta = relationship("FinanceiroContas", back_populates="lancamentos")
    conciliacoes = relationship("FinanceiroConciliacoes", back_populates="lancamento")