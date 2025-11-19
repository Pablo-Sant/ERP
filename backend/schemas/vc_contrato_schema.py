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


class ContratoRead(ContratoBase):
    contratoid: int

    class Config:
        orm_mode = True