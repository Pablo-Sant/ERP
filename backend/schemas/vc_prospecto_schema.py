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


class ProspectoRead(ProspectoBase):
    prospectoid: int

    class Config:
        orm_mode = True