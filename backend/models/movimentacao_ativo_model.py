from sqlalchemy.dialects.postgresql import UUID, JSONB
from core.configs import DBBaseModel
from sqlalchemy import (
    Column, Integer, String, Text, Date, Numeric, Boolean,
    ForeignKey, DateTime, JSON, CheckConstraint, text, func, orm
)
from typing import List


class MovimentacaoAtivo(DBBaseModel):
    __tablename__ = "movimentacoes_ativos"
    __table_args__ = (
        CheckConstraint(
            "tipo_movimentacao IN ('transferencia','implantacao','retorno','baixa')"
        ),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Relacionamento com Ativo
    id_ativo = Column(Integer, ForeignKey("am.ativos.id"), nullable=False)
    ativo = orm.relationship('Ativo', lazy='joined')
    
    # Local origem
    id_local_origem = Column(Integer, ForeignKey('am.localizacoes.id'), nullable=False)
    local_origem = orm.relationship(
        'Localizacao', 
        foreign_keys=[id_local_origem],  # ← ESPECIFIQUE a coluna
        lazy='joined'
    )
    
    # Local destino  
    id_local_destino = Column(Integer, ForeignKey('am.localizacoes.id'), nullable=False)
    local_destino = orm.relationship(
        'Localizacao', 
        foreign_keys=[id_local_destino],  # ← ESPECIFIQUE a coluna
        lazy='joined'
    )
    
    data_movimentacao = Column(DateTime(timezone=True), server_default=func.now())
    tipo_movimentacao = Column(String(50))
    motivo = Column(Text)
    movimentado_por = Column(Integer)
    numero_referencia = Column(String(100))