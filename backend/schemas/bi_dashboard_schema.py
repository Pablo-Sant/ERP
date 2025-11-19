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
        orm_mode = True