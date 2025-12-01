from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

class HistoricoCompraBase(BaseModel):
    cliente_finalid: int
    pedidoid: Optional[int] = None
    valor_compra: Optional[Decimal] = None
    data_compra: Optional[date] = None


class HistoricoCompraCreate(HistoricoCompraBase):
    pass


class HistoricoCompraResponse(HistoricoCompraBase):
    historicoid: int

    class Config:
        orm_mode = True