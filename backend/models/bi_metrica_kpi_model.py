from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Sequence
from core.configs import DBBaseModel
from datetime import datetime

class MetricaKPI(DBBaseModel):
    __tablename__ = "metrica_kpi"
    __table_args__ = {"schema": "bi"}

    id_metrica = Column(Integer, Sequence("bi.metrica_kpi_id_metrica_seq"), primary_key=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    formula_calculo = Column(Text)
    unidade_medida = Column(String(20))
    categoria = Column(String(50))