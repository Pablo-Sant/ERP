from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, Sequence,
    CheckConstraint, BOOLEAN
)
from datetime import datetime
from core.configs import DBBaseModel



class CategoriaRisco(DBBaseModel):
    __tablename__ = "categorias_risco"
    __table_args__ = (
        CheckConstraint(
            "tipo IN ('ESTRATEGICO', 'OPERACIONAL', 'FINANCEIRO', 'COMPLIANCE', 'TECNOLOGIA')",
            name="categorias_risco_tipo_check"
        ),
        {"schema": "grc"},
    )

    id = Column(Integer, Sequence("grc.categorias_risco_id_seq"), primary_key=True)

    codigo = Column(String(20), nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    tipo = Column(String(50))
    ativo = Column(BOOLEAN, default=True)