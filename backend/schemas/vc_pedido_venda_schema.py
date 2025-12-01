from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

class PedidoVendaBase(BaseModel):
    cliente_finalid: int
    vendedorid: int
    data_prevista_entrega: Optional[date] = None
    hora: Optional[datetime.time] = None
    status: Optional[str] = None


class PedidoVendaCreate(PedidoVendaBase):
    pass


class PedidoVendaResponse(PedidoVendaBase):
    pedidoid: int

    class Config:
        orm_mode = True