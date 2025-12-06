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
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class HistoricoCompraUpdate(BaseModel):
    """Schema para atualização parcial de histórico de compra"""
    cliente_finalid: Optional[int] = None
    pedidoid: Optional[int] = None
    valor_compra: Optional[Decimal] = None
    data_compra: Optional[date] = None
    
    class Config:
        from_attributes = True