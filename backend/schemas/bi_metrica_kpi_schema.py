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
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class MetricaKPIUpdate(BaseModel):
    """Schema para atualização parcial de métrica KPI"""
    nome: Optional[str] = None
    descricao: Optional[str] = None
    formula_calculo: Optional[str] = None
    unidade_medida: Optional[str] = None
    categoria: Optional[str] = None
    
    class Config:
        from_attributes = True