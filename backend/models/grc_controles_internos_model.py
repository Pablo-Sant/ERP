from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Sequence,
    CheckConstraint
)
from core.configs import DBBaseModel



class ControleInterno(DBBaseModel):
    __tablename__ = "controles_internos"
    __table_args__ = (
        CheckConstraint(
            "categoria IN ('PREVENTIVO', 'DETECTIVO', 'CORRETIVO')",
            name="controles_internos_categoria_check"
        ),
        CheckConstraint(
            "eficacia_esperada IN ('ALTA', 'MEDIA', 'BAIXA')",
            name="controles_internos_eficacia_esperada_check"
        ),
        CheckConstraint(
            "frequencia IN ('DIARIO', 'SEMANAL', 'MENSAL', 'TRIMESTRAL', 'SEMESTRAL', 'ANUAL')",
            name="controles_internos_frequencia_check"
        ),
        {"schema": "grc"},
    )

    id = Column(Integer, Sequence("grc.controles_internos_id_seq"), primary_key=True)

    codigo = Column(String(50), nullable=False)
    nome = Column(String(200), nullable=False)
    descricao = Column(Text)
    categoria = Column(String(100))
    frequencia = Column(String(50))
    proprietario_id = Column(Integer, nullable=False)
    eficacia_esperada = Column(String(20))
    ativo = Column(Boolean, default=True)
