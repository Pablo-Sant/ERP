from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, Sequence,
    CheckConstraint
)
from datetime import datetime
from core.configs import DBBaseModel




class Auditoria(DBBaseModel):
    __tablename__ = "auditorias"
    __table_args__ = (
       
        CheckConstraint(
            "resultado IN ('APROVADO', 'APROVADO_COM_RESSALVAS', 'REPROVADO')",
            name="auditorias_resultado_check"
        ),
        CheckConstraint(
            "tipo_auditoria IN ('INTERNA', 'EXTERNA', 'ISO', 'LGPD', 'SOX', 'OUTRA')",
            name="auditorias_tipo_auditoria_check"
        ),
        {"schema": "grc"},
    )

    id = Column(Integer, Sequence("grc.auditorias_id_seq"), primary_key=True)

    codigo = Column(String(50), nullable=False)
    tipo_auditoria = Column(String(100), nullable=False)
    escopo = Column(Text, nullable=False)
    normativo_referencia = Column(String(200))

    data_planejada = Column(Date)
    data_realizacao = Column(Date)

    auditor_principal_id = Column(Integer)

    resultado = Column(String(20))
    relatorio_path = Column(Text)

    criado_em = Column(DateTime, default=datetime.now)
