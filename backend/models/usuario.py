# models/usuario.py - CORRIGIDO (remover importação circular)
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UsuarioModel(Base):
    __tablename__ = "usuarios"
    __table_args__ = {'schema': 'portal'}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    tipo_usuario = Column(String, nullable=False)
    id_referencia = Column(Integer)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    ultimo_login = Column(DateTime)
    device_id = Column(String)

    