from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class ControleInternoBase(BaseModel):
    codigo: str
    nome: str
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    frequencia: Optional[str] = None
    proprietario_id: int
    eficacia_esperada: Optional[str] = None
    ativo: Optional[bool] = True


class ControleInternoCreate(ControleInternoBase):
    pass


class ControleInternoUpdate(BaseModel):
    codigo: Optional[str] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    frequencia: Optional[str] = None
    proprietario_id: Optional[int] = None
    eficacia_esperada: Optional[str] = None
    ativo: Optional[bool] = None


class ControleInternoResponse(ControleInternoBase):
    id: int

    class Config:
        from_attributes = True
