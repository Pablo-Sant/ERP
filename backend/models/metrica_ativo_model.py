from sqlalchemy.dialects.postgresql import UUID, JSONB
from core.configs import DBBaseModel
from sqlalchemy import (
    Column, Integer, String, Text, Date, Numeric, Boolean,
    ForeignKey, DateTime, JSON, CheckConstraint, text, func, orm
)
from typing import List

class MetricaAtivo(DBBaseModel):
    __tablename__ = "metricas_ativos"
    __table_args__ = {"schema": "am"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_organizacao = Column(Integer, nullable=False)
    organizacao = orm.relationship('Organizacao', lazy='joined')
    data_metrica = Column(Date, nullable=False)
    tipo_metrica = Column(String(50), nullable=False)
    valor = Column(Numeric(18, 4), nullable=False)
    valor_meta = Column(Numeric(18, 4))