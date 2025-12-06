# sm_ticket_atendimento_model.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey,Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.configs import DBBaseModel

class TicketAtendimento(DBBaseModel):
    __tablename__ = "ticket_atendimento"
    __table_args__ = {"schema": "sm"}
    
    id_ticket = Column(
        Integer, 
        Sequence("sm.ticket_atendimento_id_ticket_seq"), 
        primary_key=True
    )
    id_cliente_final = Column(
        Integer, 
        ForeignKey("vc.cliente_final.cliente_finalid"), 
        nullable=False
    )
    id_pedido = Column(
        Integer, 
        ForeignKey("vc.pedidos_de_venda.pedidoid")
    )
    tipo = Column(String(50))
    assunto = Column(String(100), nullable=False)
    descricao = Column(Text)
    status = Column(String(20), default="ABERTO")
    prioridade = Column(String(20), default="NORMAL")
    data_abertura = Column(DateTime, default=func.now())
    data_resolucao = Column(DateTime)
    
    # Relationships
    cliente_final = relationship("ClienteFinal", backref="tickets_atendimento")
    pedido = relationship("PedidoVenda", backref="tickets")
    solicitacaoTroca = relationship(
        "SolicitacaoTroca", 
        back_populates="ticket",
        cascade="all, delete-orphan"
    )