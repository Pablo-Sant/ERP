# models/ps_projeto_model.py
from sqlalchemy import Column, Integer, String, Text, Date, Numeric, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class ProjetoModel(Base):
    __tablename__ = "ps_projetos"
    
    id_projeto = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    descricao = Column(Text)
    id_gerente = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    id_cliente = Column(Integer, ForeignKey("vc_cliente_final_model.id"), nullable=True)
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
    
    # Relacionamentos
    gerente = relationship("UsuarioModel", foreign_keys=[id_gerente], back_populates="projetos_gerenciados")
    cliente = relationship("ClienteFinalModel", back_populates="projetos")
    
    # Constraints de verificação
    __table_args__ = (
        CheckConstraint(
            "prioridade IN ('BAIXA', 'MEDIA', 'ALTA', 'URGENTE')",
            name="chk_prioridade_projeto"
        ),
        CheckConstraint(
            "status IN ('PLANEJAMENTO', 'EM_ANDAMENTO', 'PAUSADO', 'CONCLUIDO', 'CANCELADO')",
            name="chk_status_projeto"
        ),
        CheckConstraint(
            "porcentagem_conclusao >= 0 AND porcentagem_conclusao <= 100",
            name="chk_porcentagem_conclusao"
        ),
        CheckConstraint(
            "orcamento_total >= 0",
            name="chk_orcamento_total"
        ),
        CheckConstraint(
            "custo_real >= 0",
            name="chk_custo_real"
        ),
    )