from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime, time
from decimal import Decimal

class PedidoVendaBase(BaseModel):
    cliente_finalid: int
    vendedorid: int
    data_prevista_entrega: Optional[date] = None
    hora: Optional[time] = None  # Corrigido: datetime.time para time
    status: Optional[str] = None


class PedidoVendaCreate(PedidoVendaBase):
    pass


class PedidoVendaResponse(PedidoVendaBase):
    pedidoid: int

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class PedidoVendaUpdate(BaseModel):
    """Schema para atualização parcial de pedido de venda"""
    cliente_finalid: Optional[int] = None
    vendedorid: Optional[int] = None
    data_prevista_entrega: Optional[date] = None
    hora: Optional[time] = None
    status: Optional[str] = None
    
    class Config:
        from_attributes = True