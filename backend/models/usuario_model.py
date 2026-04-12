from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel
from datetime import datetime

class UsuarioModel(DBBaseModel):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    data_criacao = Column(DateTime, default=datetime.now())
    
    #clientes = relationship('ClienteFinal', back_populates='usuarios', cascade='all, delete-orphan')

    
    

