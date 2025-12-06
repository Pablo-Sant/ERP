from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

class ProspectoBase(BaseModel):
    produto_interesse: Optional[str] = None
    fase_funil: Optional[str] = None
    status: Optional[str] = None


class ProspectoCreate(ProspectoBase):
    pass


class ProspectoResponse(ProspectoBase):
    prospectoid: int

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class ProspectoUpdate(BaseModel):
    """Schema para atualização parcial de prospecto"""
    produto_interesse: Optional[str] = None
    fase_funil: Optional[str] = None
    status: Optional[str] = None
    
    class Config:
        from_attributes = True