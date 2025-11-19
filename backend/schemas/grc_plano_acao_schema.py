from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class PlanoAcaoBase(BaseModel):
    risco_id: int
    descricao: str
    tipo_acao: Optional[str] = None
    responsavel_id: int
    data_prevista_conclusao: Optional[date] = None
    data_conclusao: Optional[date] = None
    status: Optional[str] = "PENDENTE"
    custo_estimado: Optional[Decimal] = None
    evidencia_conclusao: Optional[str] = None


class PlanoAcaoCreate(PlanoAcaoBase):
    pass


class PlanoAcaoUpdate(BaseModel):
    risco_id: Optional[int] = None
    descricao: Optional[str] = None
    tipo_acao: Optional[str] = None
    responsavel_id: Optional[int] = None
    data_prevista_conclusao: Optional[date] = None
    data_conclusao: Optional[date] = None
    status: Optional[str] = None
    custo_estimado: Optional[Decimal] = None
    evidencia_conclusao: Optional[str] = None


class PlanoAcaoResponse(PlanoAcaoBase):
    id: int

    class Config:
        from_attributes = True
