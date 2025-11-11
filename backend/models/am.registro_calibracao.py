from sqlalchemy import (
    Column, Integer, String, Numeric, Date, Boolean, Text, CheckConstraint, ForeignKey, Computed
)
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel
from models.ativos_model import Ativo

class RegistrosCalibracao(DBBaseModel):
    __tablename__ = "registros_calibracao"
    __table_args__ = (
        CheckConstraint(
            "condicao_encontrada IN ('dentro_especificacao','fora_especificacao','ajustado')",
            name="registros_calibracao_condicao_encontrada_check"
        ),
        CheckConstraint(
            "condicao_final IN ('dentro_especificacao','fora_especificacao')",
            name="registros_calibracao_condicao_final_check"
        ),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_ativo = Column(Integer, ForeignKey("am.ativos.id"), nullable=False)
    data_calibracao = Column(Date, nullable=False)
    data_proxima_calibracao = Column(Date, nullable=False)
    calibrado_por = Column(String(255))
    numero_certificado = Column(String(100))
    padrao_utilizado = Column(String(255))
    condicao_encontrada = Column(String(50))
    condicao_final = Column(String(50))
    incerteza = Column(Numeric(10, 6))
    calibracao_aprovada = Column(Boolean)
    observacoes = Column(Text)

    ativo = relationship("Ativo", back_populates="registros_calibracao") 