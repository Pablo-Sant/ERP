from sqlalchemy import Column, Integer, String, Text, Date, Numeric, DateTime
from sqlalchemy.sql import func
from core.database import Base

class ProjetoModel(Base):
    __tablename__ = "projetos"
    __table_args__ = {"schema": "ps"}
    
    # COLUNAS REAIS DO SEU BANCO
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
    porcentagem_conclusao = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())
    
    # PROPRIEDADES PARA COMPATIBILIDADE (opcional)
    @property
    def id(self):
        """Alias para id_projeto para compatibilidade com código existente"""
        return self.id_projeto