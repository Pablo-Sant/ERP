# models/cliente.py
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from core.database import Base
from datetime import datetime

class ClienteModel(Base):
    __tablename__ = "clientes"
    # Se clientes estiver em schema diferente:
    # __table_args__ = {'schema': 'seu_schema'}
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    nome_fantasia = Column(String(200))
    cnpj = Column(String(20), unique=True)
    email = Column(String(200))
    telefone = Column(String(20))
    endereco = Column(Text)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)