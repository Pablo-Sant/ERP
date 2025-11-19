from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Sequence
from core.configs import DBBaseModel
from datetime import datetime

class Dashboard(DBBaseModel):
    __tablename__ = "dashboard"
    __table_args__ = {"schema": "bi"}

    id_dashboard = Column(Integer, Sequence("bi.dashboard_id_dashboard_seq"), primary_key=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    config_json = Column(JSON)
    data_atualizacao = Column(DateTime, default=datetime.utcnow)