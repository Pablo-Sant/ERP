from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class SegregacaoFuncoesBase(BaseModel):
    funcao_1: str
    funcao_2: str
    conflito_nivel: Optional[str] = None
    justificativa: Optional[str] = None
    aprovado: Optional[bool] = False
    data_aprovacao: Optional[date] = None


class SegregacaoFuncoesCreate(SegregacaoFuncoesBase):
    pass


class SegregacaoFuncoesUpdate(BaseModel):
    funcao_1: Optional[str] = None
    funcao_2: Optional[str] = None
    conflito_nivel: Optional[str] = None
    justificativa: Optional[str] = None
    aprovado: Optional[bool] = None
    data_aprovacao: Optional[date] = None


class SegregacaoFuncoesResponse(SegregacaoFuncoesBase):
    id: int

    class Config:
        from_attributes = True
