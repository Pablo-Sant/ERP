# sm_solicitacao_troca_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SolicitacaoTrocaBase(BaseModel):
    id_ticket: int
    id_item_pedido: int
    motivo: Optional[str] = None
    status: Optional[str] = "SOLICITADA"
    data_solicitacao: Optional[datetime] = None

class SolicitacaoTrocaCreate(SolicitacaoTrocaBase):
    pass

class SolicitacaoTrocaResponse(SolicitacaoTrocaBase):
    id_solicitacao: int
    
    class Config:
        orm_mode = True
        from_attributes = True

class SolicitacaoTrocaUpdate(BaseModel):
    motivo: Optional[str] = None
    status: Optional[str] = None