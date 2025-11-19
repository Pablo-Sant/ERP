from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class RiscoControleBase(BaseModel):
    risco_id: int
    controle_id: int
    eficacia_mitigacao: Optional[str] = None
    observacoes: Optional[str] = None


class RiscoControleCreate(RiscoControleBase):
    pass


class RiscoControleUpdate(BaseModel):
    risco_id: Optional[int] = None
    controle_id: Optional[int] = None
    eficacia_mitigacao: Optional[str] = None
    observacoes: Optional[str] = None


class RiscoControleResponse(RiscoControleBase):
    id: int

    class Config:
        from_attributes = True
