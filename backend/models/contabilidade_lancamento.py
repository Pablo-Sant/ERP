from sqlalchemy import Column, Integer, String, Date, Text, Numeric, Boolean, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel


class ContabilidadeLancamentos(DBBaseModel):
    __tablename__ = "contabilidade_lancamentos"
    __table_args__ = {'schema': 'fi'}

    id_lancamento = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    historico = Column(Text)
    valor = Column(Numeric(14, 2), nullable=False)
    debito_conta_id = Column(Integer, ForeignKey("fi.contabilidade_plano_contas.id_conta"), nullable=False)
    credito_conta_id = Column(Integer, ForeignKey("fi.contabilidade_plano_contas.id_conta"), nullable=False)
    origem_modulo = Column(String(50))
    origem_id = Column(Integer)

    conta_debito = relationship(
        "ContabilidadePlanoContas",
        foreign_keys=[debito_conta_id],
        back_populates="lancamentos_debito"
    )
    conta_credito = relationship(
        "ContabilidadePlanoContas",
        foreign_keys=[credito_conta_id],
        back_populates="lancamentos_credito"
    )