# models/projeto_model.py - OPÇÃO SIMPLES
from sqlalchemy import Column, Integer, String, Text, Date, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class ProjetoModel(Base):
    # Defina o schema diretamente no nome da tabela
    __tablename__ = "ps.projetos"  # Schema incluído no nome
    
    # Remova o __table_args__ completamente por enquanto
    # __table_args__ = ...
    
    id_projeto = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    descricao = Column(Text)
    id_gerente = Column(Integer, nullable=True)
    id_cliente = Column(Integer, nullable=True)
    data_inicio_prevista = Column(Date)
    data_fim_prevista = Column(Date)
    data_inicio_real = Column(Date, nullable=True)
    data_fim_real = Column(Date, nullable=True)
    orcamento_total = Column(Numeric(15, 2), default=0)
    custo_real = Column(Numeric(15, 2), default=0)
    status = Column(String(50), default="PLANEJAMENTO")
    prioridade = Column(String(20), default="MEDIA")
    porcentagem_conclusao = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())