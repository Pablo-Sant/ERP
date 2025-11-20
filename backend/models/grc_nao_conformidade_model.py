from sqlalchemy import (
    Column, Integer, String, Text, Date,
    ForeignKey, CheckConstraint
)
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class NaoConformidadeAuditoria(DBBaseModel):
    __tablename__ = "nao_conformidades_auditoria"
    __table_args__ = (
        CheckConstraint(
            "classificacao IN ('CRITICA', 'MAIOR', 'MENOR')",
            name="nao_conformidades_auditoria_classificacao_check"
        ),
        CheckConstraint(
            "status IN ('ABERTA', 'EM_CORRECAO', 'VERIFICADA', 'FECHADA')",
            name="nao_conformidades_auditoria_status_check"
        ),
        {"schema": "grc"}
    )

    id = Column(Integer, primary_key=True)
    auditoria_id = Column(
        Integer,
        ForeignKey("grc.auditorias.id"),
        nullable=False
    )

    descricao = Column(Text, nullable=False)
    requisito_nao_atendido = Column(String(200))
    classificacao = Column(String(50))
    prazo_correcao = Column(Date)


    data_correcao = Column(Date)
    evidencia_correcao = Column(Text)

    status = Column(String(20), default="ABERTA", nullable=False)

    
    auditoria = relationship("Auditoria", lazy="joined")
   

