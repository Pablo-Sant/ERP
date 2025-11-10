from pydantic import BaseModel
from datetime import date
from typing import Optional

class MetricaAtivoBase(BaseModel):
    id_organizacao: int
    data_metrica: date
    tipo_metrica: str
    valor: float
    valor_meta: Optional[float]

class MetricaAtivoCreate(MetricaAtivoBase):
    pass

class MetricaAtivoResponse(MetricaAtivoBase):
    id: int

    class Config:
        orm_mode = True
