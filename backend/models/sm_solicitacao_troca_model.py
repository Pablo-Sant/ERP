# sm_solicitacao_troca_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.configs import DBBaseModel

class SolicitacaoTroca(DBBaseModel):
    __tablename__ = "solicitacaoTroca"
    __table_args__ = {"schema": "sm"}
    
    id_solicitacao = Column(
        Integer, 
        Sequence("sm.solicitacao_troca_id_solicitacao_seq"), 
        primary_key=True
    )
    id_ticket = Column(
        Integer, 
        ForeignKey("sm.ticket_atendimento.id_ticket"), 
        nullable=False
    )
    id_item_pedido = Column(Integer, nullable=False)
    motivo = Column(String(100))
    status = Column(String(20), default="SOLICITADA")
    data_solicitacao = Column(DateTime, default=func.now())

    
    ticket = relationship("TicketAtendimento", back_populates="solicitacoes_troca")
