from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, Sequence,
    CheckConstraint, ForeignKey, Numeric
)
from datetime import datetime
from core.configs import DBBaseModel

class OrdemInspecao(DBBaseModel):
    __tablename__ = "ordens_inspecao"
    __table_args__ = (
        CheckConstraint(
            "status IN ('PENDENTE', 'EM_INSPECAO', 'CONCLUIDA', 'CANCELADA')",
            name="ordens_inspecao_status_check"
        ),
        CheckConstraint(
            "tipo_origem IN ('ORDEM_PRODUCAO', 'PEDIDO_COMPRA', 'RECEBIMENTO', 'CLIENTE')",
            name="ordens_inspecao_tipo_origem_check"
        ),
        {"schema": "qm"},
    )

    id = Column(Integer, Sequence("qm.ordens_inspecao_id_seq"), primary_key=True)
    numero_oi = Column(String(50), nullable=False)
    plano_inspecao_id = Column(Integer, nullable=False)
    produto_id = Column(Integer, nullable=False)
    lote = Column(String(100))
    quantidade_inspecionar = Column(Integer, nullable=False)
    tipo_origem = Column(String(50))
    origem_id = Column(Integer)
    data_inspecao = Column(Date, default=datetime.utcnow)
    inspetor_id = Column(Integer)
    status = Column(String(20), default="PENDENTE")