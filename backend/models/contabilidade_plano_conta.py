from sqlalchemy import Column, Integer, String, Date, Text, Numeric, Boolean, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class ContabilidadePlanoContas(DBBaseModel):
    __tablename__ = "contabilidade_plano_contas"
    __table_args__ = {'schema': 'fi'}

    id_conta = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(20), nullable=False)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)
    nivel = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("tipo IN ('Ativo','Passivo','Receita','Despesa')", name="contabilidade_plano_contas_tipo_check"),
        {'schema': 'fi'}
    )

    lancamentos_debito = relationship(
        "ContabilidadeLancamentos",
        foreign_keys="[ContabilidadeLancamentos.debito_conta_id]",
        back_populates="conta_debito"
    )
    lancamentos_credito = relationship(
        "ContabilidadeLancamentos",
        foreign_keys="[ContabilidadeLancamentos.credito_conta_id]",
        back_populates="conta_credito"
    )