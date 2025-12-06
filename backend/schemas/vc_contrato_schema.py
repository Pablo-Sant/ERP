from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

class ContratoBase(BaseModel):
    cliente_finalid: Optional[int] = None
    vendedorid: Optional[int] = None
    data_inicio: Optional[datetime] = None
    vencimento: Optional[date] = None


class ContratoCreate(ContratoBase):
    cliente_finalid: int
    vendedorid: int


class ContratoResponse(ContratoBase):
    contratoid: int

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class ContratoUpdate(BaseModel):
    """Schema para atualização parcial de contrato"""
    cliente_finalid: Optional[int] = None
    vendedorid: Optional[int] = None
    data_inicio: Optional[datetime] = None
    vencimento: Optional[date] = None
    
    class Config:
        from_attributes = True