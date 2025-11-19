from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Sequence
from core.configs import DBBaseModel
from datetime import datetime

class CacheDadosBI(DBBaseModel):
    __tablename__ = "cache_dados_bi"
    __table_args__ = {"schema": "bi"}

    id_cache = Column(Integer, Sequence("bi.cache_dados_bi_id_cache_seq"), primary_key=True)
    chave_cache = Column(String(100))
    dados_json = Column(JSON)
    data_geracao = Column(DateTime, default=datetime.now)
    data_expiracao = Column(DateTime)

