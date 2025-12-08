
from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date, CheckConstraint
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class FinanceiroContas(DBBaseModel):
    __tablename__ = "financeiro_contas"
    
    __table_args__ = (
        CheckConstraint(
            "tipo IN ('caixa', 'banco', 'cartao')",
            name="financeiro_contas_tipo_check"
        ),
        {'schema': 'fi'}
    )
    
    id_conta = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)  # 'caixa', 'banco', 'cartao'
    saldo_inicial = Column(Numeric(14, 2), nullable=False, default=0)
    data_abertura = Column(Date, nullable=False)  # ADICIONE ESTE CAMPO
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
   # orcamentos = relationship("FinanceiroOrcamentos", back_populates="conta", lazy='dynamic')
   # lancamentos = relationship("FinanceiroLancamentos", back_populates="conta", lazy='dynamic')
   # extratos = relationship("FinanceiroExtratosBancarios", back_populates="conta", lazy='dynamic')