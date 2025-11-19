from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, Sequence,
    CheckConstraint, ForeignKey
)
from datetime import datetime
from core.configs import DBBaseModel

class RiscoCorporativo(DBBaseModel):
    __tablename__ = "riscos_corporativos"
    __table_args__ = (
        CheckConstraint("impacto >= 1 AND impacto <= 5", name="riscos_corporativos_impacto_check"),
        CheckConstraint("probabilidade >= 1 AND probabilidade <= 5", name="riscos_corporativos_probabilidade_check"),
        CheckConstraint(
            "status IN ('ATIVO', 'INATIVO', 'MITIGADO', 'RESOLVIDO')",
            name="riscos_corporativos_status_check"
        ),
        {"schema": "grc"},
    )

    id = Column(Integer, Sequence("grc.riscos_corporativos_id_seq"), primary_key=True)
    codigo = Column(String(50), nullable=False)
    categoria_risco_id = Column(Integer, nullable=False)
    descricao = Column(Text, nullable=False)
    causa = Column(Text)
    consequencia = Column(Text)
    probabilidade = Column(Integer)
    impacto = Column(Integer)
    severidade = Column(Integer)
    proprietario_id = Column(Integer, nullable=False)
    data_identificacao = Column(Date, default=datetime.now)
    status = Column(String(20), default="ATIVO")
    criado_em = Column(DateTime, default=datetime.now)
    criado_por = Column(Integer)