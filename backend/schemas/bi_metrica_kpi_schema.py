from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class MetricaKPIBase(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    formula_calculo: Optional[str] = None
    unidade_medida: Optional[str] = None
    categoria: Optional[str] = None


class MetricaKPICreate(MetricaKPIBase):
    nome: str


class MetricaKPIRead(MetricaKPIBase):
    id_metrica: int

    class Config:
        orm_mode = True