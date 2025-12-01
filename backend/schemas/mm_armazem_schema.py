from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ArmazemBase(BaseModel):
    empresa_id: int
    nome: str
    endereco: Optional[str] = None

class ArmazemCreate(ArmazemBase):
    pass

class ArmazemUpdate(BaseModel):
    empresa_id: Optional[int] = None
    nome: Optional[str] = None
    endereco: Optional[str] = None

class ArmazemResponse(ArmazemBase):
    id: int
    empresa_id: int
    nome: str
    endereco: str
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        orm_mode = True
