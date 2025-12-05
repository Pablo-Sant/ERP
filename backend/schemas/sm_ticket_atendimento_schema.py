# sm_ticket_atendimento_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketAtendimentoBase(BaseModel):
    id_cliente_final: int
    id_pedido: Optional[int] = None
    tipo: Optional[str] = None
    assunto: str
    descricao: Optional[str] = None
    status: Optional[str] = "ABERTO"
    prioridade: Optional[str] = "NORMAL"
    data_abertura: Optional[datetime] = None
    data_resolucao: Optional[datetime] = None

class TicketAtendimentoCreate(TicketAtendimentoBase):
    pass

class TicketAtendimentoResponse(TicketAtendimentoBase):
    id_ticket: int
    
    class Config:
        orm_mode = True
        from_attributes = True

class TicketAtendimentoUpdate(BaseModel):
    tipo: Optional[str] = None
    status: Optional[str] = None
    prioridade: Optional[str] = None
    descricao: Optional[str] = None
    data_resolucao: Optional[datetime] = None