from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class CategoriaRiscoBase(BaseModel):
    codigo: str
    nome: str
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    ativo: Optional[bool] = True


class CategoriaRiscoCreate(CategoriaRiscoBase):
    pass


class CategoriaRiscoUpdate(BaseModel):
    codigo: Optional[str] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    ativo: Optional[bool] = None


class CategoriaRiscoResponse(CategoriaRiscoBase):
    id: int

    class Config:
        from_attributes = True
