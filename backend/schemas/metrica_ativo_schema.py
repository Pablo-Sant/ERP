from pydantic import BaseModel
from datetime import date
from typing import Optional

class MetricaAtivoBase(BaseModel):
    id_organizacao: int
    data_metrica: date
    tipo_metrica: str
    valor: float
    valor_meta: Optional[float] = None


class MetricaAtivoCreate(MetricaAtivoBase):
    pass


class MetricaAtivoResponse(MetricaAtivoBase):
    id: int

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class MetricaAtivoUpdate(BaseModel):
    """Schema para atualização parcial de métrica de ativo"""
    id_organizacao: Optional[int] = None
    data_metrica: Optional[date] = None
    tipo_metrica: Optional[str] = None
    valor: Optional[float] = None
    valor_meta: Optional[float] = None
    
    class Config:
        from_attributes = True