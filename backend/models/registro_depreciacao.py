from sqlalchemy import (
    Column, Integer, String, Numeric, Date, Boolean, Text, CheckConstraint, ForeignKey, Computed
)
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel
from models.ativos_model import Ativo

class RegistrosDepreciacao(DBBaseModel):
    __tablename__ = "registros_depreciacao"
    __table_args__ = (
        CheckConstraint("depreciacao_acumulada >= 0", name="registros_depreciacao_depreciacao_acumulada_check"),
        CheckConstraint("valor_depreciacao >= 0", name="registros_depreciacao_valor_depreciacao_check"),
        CheckConstraint("valor_liquido_contabil >= 0", name="registros_depreciacao_valor_liquido_contabil_check"),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_ativo = Column(Integer, ForeignKey("am.ativos.id"), nullable=False)
    ano_fiscal = Column(Integer, nullable=False)
    periodo = Column(Integer, nullable=False)
    valor_depreciacao = Column(Numeric(18, 2), nullable=False)
    depreciacao_acumulada = Column(Numeric(18, 2), nullable=False)
    valor_liquido_contabil = Column(Numeric(18, 2), nullable=False)
    data_calculo = Column(Date, nullable=False)
    referencia_lancamento = Column(String(100))

    ativo = relationship("Ativo", back_populates="registros_depreciacao")