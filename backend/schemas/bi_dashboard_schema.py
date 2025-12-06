from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class DashboardBase(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    config_json: Optional[Any] = None
    data_atualizacao: Optional[datetime] = None


class DashboardCreate(DashboardBase):
    nome: str


class DashboardRead(DashboardBase):
    id_dashboard: int

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class DashboardUpdate(BaseModel):
    """Schema para atualização parcial de dashboard"""
    nome: Optional[str] = None
    descricao: Optional[str] = None
    config_json: Optional[Any] = None
    data_atualizacao: Optional[datetime] = None
    
    class Config:
        from_attributes = True