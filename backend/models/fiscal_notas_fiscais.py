from sqlalchemy import Column, Integer, String, Date, Text, Numeric, Boolean, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel
from models.fiscal_impostos import FiscalImpostos

class FiscalNotasFiscais(DBBaseModel):
    __tablename__ = "fiscal_notas_fiscais"
    __table_args__ = {'schema': 'fi'}

    id_nota = Column(Integer, primary_key=True, autoincrement=True)
    numero_nota = Column(String(50), nullable=False)
    tipo = Column(String(10), nullable=False)
    valor_total = Column(Numeric(14, 2), nullable=False)
    data_emissao = Column(Date, nullable=False)
    chave_acesso = Column(String(100))
    status = Column(String(20), default="ativa")

    __table_args__ = (
        CheckConstraint("status IN ('ativa','cancelada')", name="fiscal_notas_fiscais_status_check"),
        CheckConstraint("tipo IN ('entrada','saida')", name="fiscal_notas_fiscais_tipo_check"),
        {'schema': 'fi'}
    )

    impostos = relationship("FiscalImpostos", back_populates="nota")