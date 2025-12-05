# sm_atendente_model.py
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class Atendente(DBBaseModel):
    __tablename__ = "atendente"
    __table_args__ = {"schema": "sm"}
    
    id_atendente = Column(
        Integer, 
        Sequence("sm.atendente_id_atendente_seq"), 
        primary_key=True
    )
    nome = Column(String(100), nullable=False)
    email = Column(String(100))
    setor = Column(String(50))